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
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Literal

from pandas import DataFrame, read_csv, to_datetime
from pydantic import Field, model_validator, PrivateAttr

from pyswap.components.irrigation import FixedIrrigation
from pyswap.components.simsettings import RichardsSettings
from pyswap.components.soilwater import (
    SnowAndFrost,
)
from pyswap.core.io.io_ascii import open_ascii
from pyswap.components.transport import HeatFlow, SoluteTransport
from pyswap.core.defaults import IS_WINDOWS
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import SerializableMixin, FileMixin
from pyswap.libs import swap_linux, swap_windows
from pyswap.model.result import Result
from pyswap.core.fields import Subsection

logger = logging.getLogger(__name__)
__all__ = ["Model"]


class ModelBuilder:
    """Building model components.

    Attributes:
        model (Model): The model to build.
        tempdir (str): The temporary directory to store the input files.

    Methods:
        copy_executable: Copy the appropriate SWAP executable to the
            temporary directory.
        write_inputs: Write the input files to the temporary directory.
    """

    def __init__(self, model: Model, tempdir: str):
        self.model = model
        self.tempdir = tempdir

    def copy_executable(self) -> None:
        """Copy the appropriate SWAP executable to the temporary directory."""
        if IS_WINDOWS:
            shutil.copy(swap_windows, self.tempdir)
            logger.info(
                "Copying the windows version of SWAP into temporary directory..."
            )
        else:
            shutil.copy(swap_linux, self.tempdir)
            logger.info("Copying linux executable into temporary directory...")

        return self

    def write_inputs(self) -> None:
        """Write the input files to the temporary directory."""
        logger.info("Preparing files...")

        self.model.write_swp(self.tempdir)

        if self.model.lateraldrainage.drafile:
            self.model.lateraldrainage.write_dra(self.tempdir)
        if self.model.crop.cropfiles:
            self.model.crop.write_crop(self.tempdir)
        if self.model.meteorology.metfile:
            self.model.meteorology.write_met(self.tempdir)
        if self.model.fixedirrigation.irgfile:
            self.model.fixedirrigation.write_irg(self.tempdir)
        if self.model.bottomboundary.swbbcfile:
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
    def run_swap(tempdir: Path) -> str:
        """Run the SWAP executable.

        Run the exacutable in the tempdirectory and pass the newline to the
        stdin when the executable asks for input (upon termination).

        Parameters:
            tempdir (Path): The temporary directory where the executable
                is stored.
        """
        swap_path = Path(tempdir, "swap.exe") if IS_WINDOWS else "./swap420"
        p = subprocess.Popen(
            swap_path,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=tempdir,
        )
        stdout = p.communicate(input=b"\n")[0]

        return stdout.decode()

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
            builder.copy_executable().write_inputs()

            result = self.run_swap(tempdir)

            if "normal completion" not in result:
                raise Exception(f"Model run failed. \n {result}")

            logger.info(result)

            # --- Handle the results ---
            result = Result()

            reader = ResultReader(self.model, tempdir)

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
            dict: A dictionary of the output strings with extension as key.
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
    any of the components are missing.

    Attributes:
        metadata (Subsection): Metadata of the model.
        version (str): The version of the model.
        generalsettings (Subsection): Simulation settings.
        meteorology (Subsection): Meteorological data.
        crop (Subsection): Crop data.
        fixedirrigation (Subsection): Fixed irrigation settings.
        soilmoisture (Subsection): Soil moisture data.
        surfaceflow (Subsection): Surface flow data.
        evaporation (Subsection): Evaporation data.
        soilprofile (Subsection): Soil profile data.
        snowandfrost (Subsection): Snow and frost data.
        richards (Subsection): Richards data.
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

    metadata: Subsection | None = None
    version: str = Field(exclude=True, default="base")
    generalsettings: Subsection | None = None
    meteorology: Subsection | None = None
    crop: Subsection | None = None
    fixedirrigation: Subsection | None = FixedIrrigation(swirfix=0)
    soilmoisture: Subsection | None = None
    surfaceflow: Subsection | None = None
    evaporation: Subsection | None = None
    soilprofile: Subsection | None = None
    snowandfrost: Subsection | None = SnowAndFrost(swsnow=0, swfrost=0)
    richards: Subsection | None = RichardsSettings(swkmean=1, swkimpl=0)
    lateraldrainage: Subsection | None = None
    bottomboundary: Subsection | None = None
    heatflow: Subsection | None = HeatFlow(swhea=0)
    solutetransport: Subsection | None = SoluteTransport(swsolu=0)

    @property
    def swp(self):
        """The content of the swp file.

        Serialization of Subsection field type has been set in a way that it
        will generate SWAP formatted string when `model_string()` is called on
        the parent class.
        """
        return self.model_string()

    @model_validator(mode="after")
    def validate_all_components(self):
        """Validate, on run, that all required components are present."""

        if not self._validate_on_run:
            return self

        required_components = [
            "metadata",
            "generalsettings",
            "meteorology",
            "crop",
            "fixedirrigation",
            "soilmoisture",
            "surfaceflow",
            "evaporation",
            "soilprofile",
            "snowandfrost",
            "richards",
            "lateraldrainage",
            "bottomboundary",
            "heatflow",
            "solutetransport",
        ]

        missing_components = [
            comp for comp in required_components if getattr(self, comp) is None
        ]

        if missing_components:
            raise ValueError(
                f"Missing required components: {', '.join(missing_components)}"
            )

        return self

    def validate(self):
        """Execute the model validation when `run()` is called."""

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

    def to_classic_swap(self, path: Path) -> None:
        """Prepare all the files for a model run in user's directory."""
        self.validate()
        builder = ModelBuilder(model=self, tempdir=path)

        builder.write_inputs()
        builder.copy_executable()

        logger.info(f"Model files written to {path}")

    def run(self, path: str | Path, silence_warnings: bool = False):
        """Run the model using ModelRunner."""
        self.validate()
        return ModelRunner(self).run(path, silence_warnings)
