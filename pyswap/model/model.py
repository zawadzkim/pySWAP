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

    ModelBuilder: Class responsible for building the model components.
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
        """Write the input files to the temporary directory."""
        logger.info("Preparing files...")

        self.model.write_swp(self.tempdir)

        if self.model.lateraldrainage.swdra in [1, 2]:
            self.model.lateraldrainage.write_dra(self.tempdir)
        if self.model.crop.cropfiles:
            self.model.crop.write_crop(self.tempdir)
            # Check if co2correction is used in any of the cropfiles
            crops_co2corrections = [
                cropfile.co2correction is not None
                for cropfile in self.model.crop.cropfiles.values()
            ]
            # If so, copy the co2correction file to the tempdir
            if sum(crops_co2corrections) > 0:
                co2db = CO2concentration()
                period = [
                    self.model.generalsettings.tstart,
                    self.model.generalsettings.tend,
                ]
                co2db.write_co2(self.tempdir, period)
        if self.model.meteorology.metfile:
            self.model.meteorology.write_met(self.tempdir)
        if self.model.fixedirrigation.swirgfil == 1:
            self.model.fixedirrigation.write_irg(self.tempdir)
        if self.model.bottomboundary.swbbcfile == 1:
            self.model.bottomboundary.write_bbc(self.tempdir)

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
    def run_swap(tempdir: Path) -> tuple[str, str, int]:
        """Run the SWAP executable.

        Run the exacutable in the tempdirectory and pass the newline to the
        stdin when the executable asks for input (upon termination).

        get_swap will now automatically install the SWAP executable if it is not found and
        return the path to the executable.

        Parameters:
            tempdir (Path): The temporary directory where the executable
                is stored.

        Returns:
            tuple[str, str, int]: stdout, stderr, and return code

        Raises:
            RuntimeError: If the executable cannot be run (e.g., wrong architecture,
                not executable, corrupt file).
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
            stdout, stderr = p.communicate(input=b"\n")
            return stdout.decode(), stderr.decode(), p.returncode
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

    def run(self, path: str | Path, silence_warnings: bool = False) -> Result:
        """Main function that runs the model.

        First ModelBuilder is used to prepare the environment for the model run.
        Second, the SWAP executable is run and the decoded result passed from
        the executable is parsed using the ResultReader and used to update the
        Result object.

        Parameters:
            path (str | Path): The path to the temporary directory.
            silence_warnings (bool): If True, warnings are not raised.

        Returns:
            Result: The parsed model results.
        """

        with tempfile.TemporaryDirectory(dir=path) as tempdir:
            builder = ModelBuilder(self.model, tempdir)

            builder.write_inputs()

            stdout, stderr, returncode = self.run_swap(tempdir)
            reader = ResultReader(self.model, tempdir)

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
        default=RichardsSettings(swkmean=1, swkimpl=0), repr=False
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

    def to_classic_swap(self, path: Path) -> None:
        """Prepare all the files for a model run in user's directory."""
        self.validate()
        builder = ModelBuilder(model=self, tempdir=path)

        builder.write_inputs()

        logger.info(f"Model files written to {path}")

    def run(
        self, path: str | Path | None = None, silence_warnings: bool = False
    ) -> Result:
        """Run the model using ModelRunner."""
        self.validate()
        path = Path.cwd() if path is None else path
        return ModelRunner(self).run(path, silence_warnings)


def _run_model_with_params(args) -> Result:
    """Helper function to run a model with parameters."""
    model, path, silence_warnings = args
    return model.run(path=path, silence_warnings=silence_warnings)


def run_parallel(
    mls: list[Model],
    path: Path | str | None = None,
    silence_warnings: bool = False,
    **kwargs,
) -> list[Result]:
    """Run multiple models in parallel.

    Parameters:
        mls (list[Model]): List of models to run.
        path (Path | str): The path to the temporary directory.
        silence_warnings (bool): If True, warnings are not raised.
        **kwargs (dict): Keyword arguments for Pool().

    Returns:
        list[Result]: List of results from the model runs.
    """
    with Pool(**kwargs) as pool:
        results = pool.map(
            _run_model_with_params, [(model, path, silence_warnings) for model in mls]
        )

    return results
