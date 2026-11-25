# mypy: disable-error-code="override, func-returns-value, call-overload, operator, no-any-return"
# Override error is related to the validate method, must have somethiong to do
# with Pydantic.
# func-returns-value is raised on the model builder, because it does not return
# anything. This is not a priority to fix.
# the operator was returned on one of the checks (swdra comparison), which is
# ok. It is validated prior to reaching that point.
# no-any-return is raised on the run_parallel function, because it returns a
# list of results. This is not a priority to fix.
# securing the subprocess call does not seem like a priority in this project
"""Building, running and parsing the results of a SWAP model run.

When the Model class begun to grow, it was clear that it needed to be refactored
into a more modular structure. The functionality to build environment, run and
parse result has been abstracted to 3 classes, focusing the main (and exposed to
the user) Model class focused on the model components and their interactions.
The four classes in this module are:

Classes:

    ModelBuilder: Collects the model's input files (writing is done by
        Model.write).
    ModelRunner: Class responsible for running the model.
    ResultReader: Class responsible for parsing the model results.
    Model: Main class that runs the SWAP model.
"""

from __future__ import annotations

import logging
import os
import subprocess
import tempfile
from multiprocessing import Pool
from pathlib import Path
from typing import Literal

from pandas import DataFrame, read_csv, to_datetime
from pydantic import Field, PrivateAttr, model_validator

from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import Crop
from pyswap.components.drainage import Drainage
from pyswap.components.irrigation import FixedIrrigation
from pyswap.components.metadata import Metadata
from pyswap.components.meteorology import Meteorology
from pyswap.components.simsettings import GeneralSettings, RichardsSettings
from pyswap.components.soilwater import (
    Evaporation,
    SnowAndFrost,
    SoilMoisture,
    SoilProfile,
    SurfaceFlow,
)
from pyswap.components.transport import HeatFlow, SoluteTransport
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import Subsection
from pyswap.core.io.io_ascii import open_ascii
from pyswap.core.io.process_ascii import parse_ascii_file
from pyswap.db.co2concentration import CO2concentration
from pyswap.model.result import Result
from pyswap.utils.executables import get_swap
from pyswap.utils.mixins import FileMixin, SerializableMixin

logger = logging.getLogger(__name__)

__all__ = ["Model", "run_parallel"]


class ModelBuilder:
    """Building model components.

    Attributes:
        model (Model): The model to build.
        tempdir (str): The temporary directory to store the input files.

        write_inputs: Write the input files to the temporary directory.
    """

    def __init__(self, model: Model, tempdir: str):
        self.model = model
        self.tempdir = tempdir

    def get_inputs(self) -> dict:
        """Get the inpup files in a dictionary."""
        inputs = {}

        inputs["swp"] = self.model.swp
        if self.model.lateraldrainage.swdra in [1, 2]:
            inputs["dra"] = self.model.lateraldrainage.drafile.dra
        if self.model.crop.cropfiles:
            inputs["crop"] = self.model.crop.cropfiles
        if self.model.meteorology.metfile:
            inputs["met"] = self.model.meteorology.met
        if self.model.fixedirrigation.swirgfil == 1:
            inputs["irg"] = self.model.fixedirrigation.irg
        if self.model.bottomboundary.swbbcfile == 1:
            inputs["bbc"] = self.model.bottomboundary.bbc

        return inputs

    def write_inputs(self) -> None:
        """Write the input files to the temporary directory.

        Kept for backwards compatibility; the writing itself is done by
        `Model.write`.
        """
        self.model.write(self.tempdir, validate=False)
        return self


class ModelRunner:
    """Class responsible for running the model.

    In the run method, the ResultReader is utilized to abstract the parsing of
    the model results.

    Attributes:
        model (Model): The model to run.

    Methods:
        run_swap: Run the SWAP executable.
        raise_swap_warning: Raise a warning.
        run: Main function that runs the model
    """

    def __init__(self, model: Model):
        self.model = model

    @staticmethod
    def run_swap(tempdir: Path, timeout: float | None = None) -> tuple[str, str, int]:
        """Run the SWAP executable.

        Run the exacutable in the tempdirectory and pass the newline to the
        stdin when the executable asks for input (upon termination).

        get_swap will now automatically install the SWAP executable if it is not found and
        return the path to the executable.

        Parameters:
            tempdir (Path): The temporary directory where the executable
                is stored.
            timeout (float | None): Maximum run time in seconds. None means
                no limit.

        Returns:
            tuple[str, str, int]: stdout, stderr, and return code

        Raises:
            RuntimeError: If the executable cannot be run (e.g., wrong architecture,
                not executable, corrupt file) or does not finish within timeout.
        """
        swap_path = get_swap(verbose=False, auto_install=True)

        try:
            p = subprocess.Popen(
                swap_path,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=tempdir,
            )
            stdout, stderr = p.communicate(input=b"\n", timeout=timeout)
            return stdout.decode(), stderr.decode(), p.returncode
        except subprocess.TimeoutExpired as e:
            p.kill()
            p.communicate()
            msg = f"SWAP did not finish within {timeout} s."
            raise RuntimeError(msg) from e
        except OSError as e:
            # This catches issues like: permission denied, exec format error (wrong architecture),
            # file not found, etc.
            msg = (
                f"Failed to execute SWAP binary at {swap_path}.\n"
                f"Error: {e}\n"
                f"This may indicate:\n"
                f"  - Wrong executable architecture (e.g., Windows binary on Linux)\n"
                f"  - Corrupted executable file\n"
                f"  - Missing executable permissions\n"
                f"  - Incompatible SWAP version"
            )
            raise RuntimeError(msg) from e
        except Exception as e:
            msg = f"Unexpected error while running SWAP executable: {e}"
            raise RuntimeError(msg) from e

    def raise_swap_warning(self, warnings: list):
        """Log the warnings form the model run.

        Parameters:
            warnings (list): The warnings from the model run parsed with the
                ResultReaded.
        """
        for message in warnings:
            logger.warning(message)

    def run(
        self,
        path: str | Path,
        silence_warnings: bool = False,
        timeout: float | None = None,
        run_dir: str | Path | None = None,
    ) -> Result:
        """Main function that runs the model.

        First ModelBuilder is used to prepare the environment for the model run.
        Second, the SWAP executable is run and the decoded result passed from
        the executable is parsed using the ResultReader and used to update the
        Result object.

        Parameters:
            path (str | Path): The directory in which the temporary run
                directory is created. Ignored when `run_dir` is given.
            silence_warnings (bool): If True, warnings are not raised.
            timeout (float | None): Maximum SWAP run time in seconds.
            run_dir (str | Path | None): Directory to write the input files to
                and run SWAP in. It is created if needed and kept after the
                run, with the inputs and all SWAP outputs. If None (default),
                a temporary directory is used and deleted after the run.

        Returns:
            Result: The parsed model results.
        """

        if run_dir is not None:
            run_dir = Path(run_dir)
            run_dir.mkdir(parents=True, exist_ok=True)
            return self._run_in(run_dir, silence_warnings, timeout)

        with tempfile.TemporaryDirectory(dir=path) as tempdir:
            return self._run_in(Path(tempdir), silence_warnings, timeout)

    def _run_in(
        self,
        workdir: Path,
        silence_warnings: bool = False,
        timeout: float | None = None,
    ) -> Result:
        """Write the inputs to `workdir`, run SWAP there and read the results."""
        self.model.write(workdir, validate=False)

        stdout, stderr, returncode = self.run_swap(workdir, timeout)
        reader = ResultReader(self.model, workdir)

        if "normal completion" not in stdout.lower():
            # Build a comprehensive error message
            error_parts = ["SWAP model run failed."]

            if returncode != 0:
                error_parts.append(f"\nReturn code: {returncode}")

                # Check for specific Windows error codes
                if returncode == 3221225781 or returncode == -1073741515:
                    # 0xC0000135 = STATUS_DLL_NOT_FOUND
                    error_parts.append(
                        "\nThis error indicates MISSING DLL FILES (Windows error 0xC0000135)."
                        "\nThe SWAP executable cannot find required runtime libraries."
                        "\nRun 'pyswap check-swap' to diagnose which DLLs are missing."
                        "\n\nCommon solution: Install Microsoft Visual C++ Redistributable:"
                        "\n  https://aka.ms/vs/17/release/vc_redist.x64.exe"
                    )

            if stderr:
                error_parts.append(f"\nStderr output:\n{stderr}")

            if stdout:
                error_parts.append(f"\nStdout output:\n{stdout}")

            # Try to read error file
            err_content = reader.read_error_file()
            if err_content:
                error_parts.append(f"\nError file (.err):\n{err_content}")

            # Try to read log file
            try:
                log = reader.read_swap_log()
                error_parts.append(f"\nLog file (.log):\n{log}")
            except FileNotFoundError:
                error_parts.append("\nLog file (.log): Not found - executable may have crashed before writing log file")

            # Try to read warning file
            wrn_content = reader.read_warning_file()
            if wrn_content:
                error_parts.append(f"\nWarning file (.wrn):\n{wrn_content}")

            msg = "\n".join(error_parts)
            logger.error(msg)
            raise RuntimeError(msg)

        logger.info(stdout)

        # --- Handle the results ---
        result: Result = Result()

        log = reader.read_swap_log()
        result.log = log

        warnings = reader.identify_warnings(log)
        result.warning = warnings

        if warnings and not silence_warnings:
            self.raise_swap_warning(warnings=warnings)

        if "csv" in self.model.generalsettings.extensions:
            output = reader.read_csv_output(which="csv")
            result.output.update({"csv": output})

        if "csv_tz" in self.model.generalsettings.extensions:
            output_tz = reader.read_csv_output(which="csv_tz")
            result.output.update({"csv_tz": output_tz})

        ascii_files = reader.read_ascii_output()

        result.output.update(ascii_files)
        return result


class ResultReader:
    """Class responsible for reading the model results.

    Attributes:
        model (Model): The model to read the results from.
        tempdir (str): The temporary directory where the results are stored.

    Methods:
        read_csv_output: Read the csv output.
        read_swap_log: Read the log files.
        identify_warnings: Catch warnings from the log file.
        read_ascii_output: Read all output files that are not in csv format
            as strings.
    """

    def __init__(self, model: Model, tempdir: str):
        self.model: Model = model
        self.tempdir = tempdir

    def read_csv_output(self, which: Literal["csv", "csv_tz"]) -> DataFrame:
        """Read the csv output.

        There are two types of csv output files: csv and csv_tz. They are both
        handle in the same method with mode change.

        Parameters:
            which (str): The type of output file to read.

        Returns:
            DataFrame: The output file as a DataFrame.
        """

        outfil = self.model.generalsettings.outfil
        output_suffix = "_output.csv" if which == "csv" else "_output_tz.csv"
        index_col = "DATETIME" if which == "csv" else "DATE"

        path = Path(self.tempdir, outfil + output_suffix)

        if not path.exists():
            logger.warning(f"Expected output file {path} not found.")
            return DataFrame()

        df = read_csv(path, comment="*", index_col=index_col)
        df.index = to_datetime(df.index)

        return df

    def read_swap_log(self) -> str:
        """Read the log files.

        Returns:
            str: The content of the log file.

        Raises:
            FileNotFoundError: If no log file is found. There should always be
                a log file. If not, something went wrong.
            FileExistsError: If multiple log files are found. Not sure if this
                is possible or not. If so, it should be handled.
        """

        log_files = [
            f for f in Path(self.tempdir).glob("*.log") if f.name != "reruns.log"
        ]

        if len(log_files) == 0:
            msg = "No .log file found in the directory."
            raise FileNotFoundError(msg)

        elif len(log_files) > 1:
            msg = "Multiple .log files found in the directory."
            raise FileExistsError(msg)

        log_file = log_files[0]

        with open(log_file) as file:
            log_content = file.read()

        return log_content

    def read_error_file(self) -> str | None:
        """Read the SWAP error file (.err).

        SWAP writes error messages to a .err file when it encounters
        fatal errors.

        Returns:
            str | None: The content of the error file, or None if not found.
        """
        err_files = list(Path(self.tempdir).glob("*.err"))

        if len(err_files) == 0:
            return None

        err_file = err_files[0]

        try:
            with open(err_file) as file:
                content = file.read()
            # Only return if file has content
            return content.strip() if content.strip() else None
        except Exception:
            return None

    def read_warning_file(self) -> str | None:
        """Read the SWAP warning file (.wrn).

        SWAP writes warning messages to a .wrn file during execution.

        Returns:
            str | None: The content of the warning file, or None if not found.
        """
        wrn_files = list(Path(self.tempdir).glob("*.wrn"))

        if len(wrn_files) == 0:
            return None

        wrn_file = wrn_files[0]

        try:
            with open(wrn_file) as file:
                content = file.read()
            # Only return if file has content
            return content.strip() if content.strip() else None
        except Exception:
            return None

    @staticmethod
    def identify_warnings(log: str) -> list:
        """Catch warnings from the log file.

        This is used by the ModelRunner to raise warnings after the model run.

        Parameters:
            log (str): The log file content.

        Returns:
            list: A list of warnings.
        """
        lines = log.split("\n")
        warnings = [
            line for line in lines if line.strip().lower().startswith("warning")
        ]
        return warnings

    def read_ascii_output(self):
        """Read all output files that are not csv format as strings.

        This method is perhaps a bit oversimplified. In the future, we might
        think about introducing parsers for the different output files. For now,
        we just read them as strings.

        Returns:
            dict (dict): A dictionary of the output strings with extension as key.
        """

        ascii_extensions = [
            ext
            for ext in self.model.generalsettings.extensions
            if ext not in ["csv", "csv_tz"]
        ]

        list_dir = os.listdir(self.tempdir)
        list_dir = [f for f in list_dir if f.endswith(tuple(ascii_extensions))]

        if list_dir:
            dict_files = {
                f.split(".")[1]: open_ascii(Path(self.tempdir, f)) for f in list_dir
            }
            return dict_files
        return {}


class Model(PySWAPBaseModel, FileMixin, SerializableMixin):
    """Main class that runs the SWAP model.

    Even though all sections are set to optional, the model will not run if
    any of the components are missing, except for fixedirrigation, SnowAndFrost,
    RichardsSettings, HeatFlow and SoluteTransport. These components have
    default values that will be used if they are not provided.

    Attributes:
        metadata (Subsection): Metadata of the model.
        version (str): The version of the model (default: "base").
        generalsettings (Subsection): Simulation settings.
        richardsettings (Subsection): Richards settings.
        meteorology (Subsection): Meteorological data.
        crop (Subsection): Crop data.
        fixedirrigation (Subsection): Fixed irrigation settings (default: no irrigation).
        soilmoisture (Subsection): Soil moisture data.
        surfaceflow (Subsection): Surface flow data.
        evaporation (Subsection): Evaporation data.
        soilprofile (Subsection): Soil profile data.
        snowandfrost (Subsection): Snow and frost data (default: no snow and frost).
        lateraldrainage (Subsection): Lateral drainage data.
        bottomboundary (Subsection): Bottom boundary data.
        heatflow (Subsection): Heat flow data.
        solutetransport (Subsection): Solute transport data.

    Methods:
        write_swp: Write the .swp input file.
        write: Write the .swp file and all component input files.
        load: Load a model from a .swp file and the files it references.
        validate: Validate the model.
        run: Run the model.
    """

    _validate_on_run: bool = PrivateAttr(default=False)
    _extension = "swp"

    metadata: Subsection[Metadata] | None = Field(default=None, repr=False)
    version: str = Field(exclude=True, default="base")
    generalsettings: Subsection[GeneralSettings] | None = Field(
        default=None, repr=False
    )
    richardsettings: Subsection[RichardsSettings] | None = Field(
        default=RichardsSettings(), repr=False
    )
    meteorology: Subsection[Meteorology] | None = Field(default=None, repr=False)
    crop: Subsection[Crop] | None = Field(default=None, repr=False)
    fixedirrigation: Subsection[FixedIrrigation] | None = Field(
        default=FixedIrrigation(swirfix=0), repr=False
    )
    soilmoisture: Subsection[SoilMoisture] | None = Field(default=None, repr=False)
    surfaceflow: Subsection[SurfaceFlow] | None = Field(default=None, repr=False)
    evaporation: Subsection[Evaporation] | None = Field(default=None, repr=False)
    soilprofile: Subsection[SoilProfile] | None = Field(default=None, repr=False)
    snowandfrost: Subsection[SnowAndFrost] | None = Field(
        default=SnowAndFrost(swsnow=0, swfrost=0), repr=False
    )
    lateraldrainage: Subsection[Drainage] | None = Field(default=None, repr=False)
    bottomboundary: Subsection[BottomBoundary] | None = Field(default=None, repr=False)
    heatflow: Subsection[HeatFlow] | None = Field(default=HeatFlow(swhea=0), repr=False)
    solutetransport: Subsection[SoluteTransport] | None = Field(
        default=SoluteTransport(swsolu=0), repr=False
    )

    @property
    def swp(self):
        """The content of the swp file.

        Serialization of Subsection field type has been set in a way that it
        will generate SWAP formatted string when `model_string()` is called on
        the parent class.
        """
        return self.model_string()

    @model_validator(mode="after")
    def validate_missing_components(self):
        """Validate, on run, that all required components are present."""

        if not self._validate_on_run:
            return self

        required_components = [
            "metadata",
            "generalsettings",
            "richardsettings",
            "meteorology",
            "crop",
            "fixedirrigation",
            "soilmoisture",
            "surfaceflow",
            "evaporation",
            "soilprofile",
            "snowandfrost",
            "lateraldrainage",
            "bottomboundary",
            "heatflow",
            "solutetransport",
        ]

        missing_components = [
            comp for comp in required_components if getattr(self, comp) is None
        ]

        if missing_components:
            msg = f"Missing required components: {', '.join(missing_components)}"
            raise ValueError(msg)

        # validate each component
        for comp in required_components:
            getattr(self, comp)

        return self

    @model_validator(mode="after")
    def validate_each_component(self):
        """Validate, on run, that all required components are present."""

        if not self._validate_on_run:
            return self

        for comp in Model.model_fields:
            item = getattr(self, comp)
            if hasattr(item, "validate_with_yaml"):
                item._validation = True
                item.validate_with_yaml()

        return self

    def validate(self):
        """Execute the model validation when `run()` is called.

        This method should probably be refactored. It seems to shadow some
        validation method from Pydantic.
        """

        try:
            self._validate_on_run = True
            self.model_validate(self)
        finally:
            self._validate_on_run = False
            logger.info("Validation successful.")

    def write_swp(self, path: str | Path):
        """Write the .swp input file.

        Parameters:
            path (str | Path): The path to write the file to.
        """
        self.save_file(string=self.swp, path=path, fname="swap")

    def get_inputs(self) -> dict:
        """Get the input files in a dictionary."""
        builder = ModelBuilder(model=self, tempdir=Path.cwd())
        return builder.get_inputs()

    def write(self, path: str | Path, validate: bool = True) -> Path:
        """Write the model to a directory: the .swp file and all component files.

        Writes `swap.swp` and every input file the attached components need
        (.dra, .crp, .met, .irg, .bbc and, when a crop uses CO2 correction, the
        CO2 concentration file), i.e. exactly the files `run()` gives to SWAP.
        The directory is created if it does not exist; files with the same
        names are overwritten.

        Parameters:
            path (str | Path): Directory to write the files to.
            validate (bool): Validate the model before writing (default True).

        Returns:
            Path: The directory the files were written to.
        """
        if validate:
            self.validate()
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        logger.info("Preparing files...")

        self.write_swp(path)

        if self.lateraldrainage.swdra in [1, 2]:
            self.lateraldrainage.write_dra(path)
        if self.crop.cropfiles:
            self.crop.write_crop(path)
            # Check if co2correction is used in any of the cropfiles
            crops_co2corrections = [
                cropfile.co2correction is not None
                for cropfile in self.crop.cropfiles.values()
            ]
            # If so, write the CO2 concentration file as well
            if sum(crops_co2corrections) > 0:
                co2db = CO2concentration()
                period = [
                    self.generalsettings.tstart,
                    self.generalsettings.tend,
                ]
                co2db.write_co2(path, period)
        if self.meteorology.metfile:
            self.meteorology.write_met(path)
        if self.fixedirrigation.swirgfil == 1:
            self.fixedirrigation.write_irg(path)
        if self.bottomboundary.swbbcfile == 1:
            self.bottomboundary.write_bbc(path)

        return path

    @classmethod
    def load(cls, swp_path: str | Path, metadata: Metadata | None = None) -> Model:
        """Load a model from a classic SWAP input directory, starting at its .swp file.

        Parses the .swp file and loads the files it references, looked up in
        the directory of the .swp file (where `write()` puts them):

        * crop files (.crp) listed in the crop rotation, as simple, WOFOST or
          grass crops according to CROPTYPE;
        * the drainage file (.dra) if SWDRA is 1 or 2;
        * the bottom boundary file (.bbc) if SWBBCFILE is 1;
        * the meteorological file named by METFIL if it is a single .met file.

        Not loaded (a warning is logged and the component is left for you to
        set): a separate irrigation file (SWIRGFIL = 1, no loader exists yet),
        yearly meteorological files (METFIL without the .met extension), and
        referenced files that are missing. SWAP outputs are never loaded. Paths
        in PATHATM, PATHCROP and PATHDRAIN are not followed.

        Parameters:
            swp_path (str | Path): Path to the .swp file.
            metadata (Metadata | None): Model metadata. If None, the project
                name is taken from PROJECT in the .swp file and the other
                fields are set to "unknown" (they are not written to SWAP
                input files).

        Returns:
            Model: The loaded model.
        """
        # imported here: the loaders module imports Model
        from pyswap.components.meteorology import metfile_from_csv
        from pyswap.utils.loaders import load_bbc, load_crp, load_dra, load_swp

        swp_path = Path(swp_path)
        folder = swp_path.parent
        params = parse_ascii_file(open_ascii(swp_path))

        def _name(value) -> str:
            return str(value).strip().strip("'\"").strip()

        def _find(fname: str) -> Path | None:
            for candidate in (fname, fname.lower(), fname.upper()):
                if (folder / candidate).exists():
                    return folder / candidate
            logger.warning(
                f"{fname} is referenced in {swp_path.name} but not found in {folder}; not loaded."
            )
            return None

        if metadata is None:
            metadata = Metadata(
                author="unknown",
                institution="unknown",
                email="unknown",
                project=_name(params.get("project", "unknown")),
                swap_ver="unknown",
            )

        ml = load_swp(swp_path, metadata)

        rotation = ml.crop.croprotation if ml.crop is not None else None
        if (
            ml.crop is not None
            and ml.crop.swcrop == 1
            and isinstance(rotation, DataFrame)
        ):
            crptypes = {1: "fixed", 2: "wofost", 3: "grass"}
            cropfiles = {}
            for cropfil, croptype in (
                rotation[["CROPFIL", "CROPTYPE"]]
                .drop_duplicates()
                .itertuples(index=False)
            ):
                name = _name(cropfil)
                crp_path = _find(f"{name}.crp")
                if crp_path is not None:
                    cropfiles[name] = load_crp(
                        crp_path, crptype=crptypes[int(croptype)], name=name
                    )
            ml.crop.cropfiles = cropfiles

        if ml.lateraldrainage is not None and ml.lateraldrainage.swdra in [1, 2]:
            dra_path = _find(f"{_name(ml.lateraldrainage.drfil)}.dra")
            if dra_path is not None:
                ml.lateraldrainage.drafile = load_dra(dra_path)

        if ml.bottomboundary is not None and ml.bottomboundary.swbbcfile == 1:
            bbc_path = _find(f"{_name(ml.bottomboundary.bbcfil)}.bbc")
            if bbc_path is not None:
                ml.bottomboundary = load_bbc(bbc_path, ml.bottomboundary)

        metfil = _name(params.get("metfil", ""))
        if metfil.lower().endswith(".met"):
            met_path = _find(metfil)
            if met_path is not None:
                # .met files are CSV with a header block of "*" comment lines
                header = 0
                with open(met_path) as f:
                    for line in f:
                        if not line.startswith("*"):
                            break
                        header += 1
                ml.meteorology.metfile = metfile_from_csv(
                    metfil, met_path, skiprows=header or None
                )
        elif metfil:
            logger.warning(
                f"METFIL '{metfil}' refers to yearly meteorological files, which Model.load does not read; set meteorology.metfile yourself."
            )

        if ml.fixedirrigation is not None and ml.fixedirrigation.swirgfil == 1:
            logger.warning(
                "The irrigation file (SWIRGFIL = 1) is not loaded: pySWAP has no .irg loader yet; set fixedirrigation yourself."
            )

        return ml

    def to_classic_swap(self, path: Path) -> None:
        """Prepare all the files for a model run in user's directory.

        Same as `write(path)`; kept for backwards compatibility.
        """
        self.write(path)
        logger.info(f"Model files written to {path}")

    def run(
        self,
        path: str | Path | None = None,
        silence_warnings: bool = False,
        timeout: float | None = None,
        run_dir: str | Path | None = None,
    ) -> Result:
        """Run the model using ModelRunner.

        Parameters:
            path (str | Path | None): Directory in which the temporary run
                directory is created (default: the current working directory).
                Ignored when `run_dir` is given.
            silence_warnings (bool): If True, SWAP warnings are not logged.
            timeout (float | None): Maximum SWAP run time in seconds.
            run_dir (str | Path | None): Directory to run the model in and keep
                afterwards. pySWAP writes the input files (.swp, .met, .crp,
                ...) there, runs SWAP in it and leaves all inputs and outputs in
                place, so the run can be inspected, archived or rerun with the
                SWAP executable. The directory is created if it does not exist;
                files with the same names are overwritten. If None (default),
                the model runs in a temporary directory that is deleted
                afterwards.

        Returns:
            Result: The parsed model results.
        """
        self.validate()
        path = Path.cwd() if path is None else path
        return ModelRunner(self).run(path, silence_warnings, timeout, run_dir=run_dir)


def _run_model_with_params(args) -> Result:
    """Helper function to run a model with parameters.

    Errors are returned in the Result, so that one failed run does not discard
    the results of the others.
    """
    model, path, silence_warnings, timeout = args
    try:
        return model.run(path=path, silence_warnings=silence_warnings, timeout=timeout)
    except Exception as e:
        return Result(error=str(e))


def run_parallel(
    mls: list[Model],
    path: Path | str | None = None,
    silence_warnings: bool = False,
    on_error: Literal["raise", "capture"] = "raise",
    timeout: float | None = None,
    **kwargs,
) -> list[Result]:
    """Run multiple models in parallel.

    Parameters:
        mls (list[Model]): List of models to run.
        path (Path | str): The path to the temporary directory.
        silence_warnings (bool): If True, warnings are not raised.
        on_error (Literal["raise", "capture"]): What to do when runs fail.

            * raise - Raise a RuntimeError naming the failed runs, after all
                runs have finished.
            * capture - Return a Result with `error` set for each failed run.

        timeout (float | None): Maximum run time of each SWAP run in seconds.
        **kwargs (dict): Keyword arguments for Pool().

    Returns:
        list[Result]: List of results from the model runs.
    """
    if on_error not in ("raise", "capture"):
        msg = f"on_error must be 'raise' or 'capture', got {on_error!r}"
        raise ValueError(msg)

    with Pool(**kwargs) as pool:
        results = pool.map(
            _run_model_with_params,
            [(model, path, silence_warnings, timeout) for model in mls],
        )

    failed = [i for i, result in enumerate(results) if not result.success]
    if failed and on_error == "raise":
        msg = (
            f"{len(failed)} of {len(mls)} model runs failed (indices {failed}). "
            f"Error of run {failed[0]}:\n{results[failed[0]].error}"
        )
        raise RuntimeError(msg)

    return results
