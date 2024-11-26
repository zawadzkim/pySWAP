"""The main model class.

Classes:
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

from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import Crop
from pyswap.components.drainage import Drainage
from pyswap.components.irrigation import FixedIrrigation
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
from pyswap.core import IS_WINDOWS
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import ComplexSerializableMixin, FileMixin
from pyswap.libs import swap_linux, swap_windows
from pyswap.model.metadata import Metadata
from pyswap.model.result import Result

logger = logging.getLogger(__name__)
__all__ = ["Model"]


class ModelBuilder:
    """Class responsible for building the model components."""

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

    Attributes:
        model (Model): The model to run.

    Methods:
        copy_executable: Copy the appropriate SWAP executable to the temporary directory.
        run_swap: Run the SWAP executable.
        raise_swap_warning: Raise a warning.
        run: Main function that runs the model
    """

    def __init__(self, model: Model):
        self.model = model

    @staticmethod
    def run_swap(tempdir: Path) -> str:
        """Run the SWAP executable."""
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
        """Gets the output from identify_warnings() and logs them."""
        for message in warnings:
            logger.warning(message)

    def run(self, path: str | Path, silence_warnings: bool = False):
        """Main function that runs the model."""
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

            log = reader.read_swap_log(tempdir)
            result.log = log

            warnings = reader.identify_warnings(log)
            result.warning = warnings

            if warnings and not silence_warnings:
                self.raise_swap_warning(warnings=warnings)

            if "csv" in self.model.generalsettings.extensions:
                output = reader.read_swap_csv(which="csv")
                result.output.update({"csv": output})

            if "csv_tz" in self.model.generalsettings.extensions:
                output_tz = reader.read_swap_csv(which="csv_tz")
                result.output.update({"csv_tz": output_tz})

            ascii_files = reader.read_swap_ascii()

            result.output.update(ascii_files)
            return result


class ResultReader:
    """Class responsible for reading the model results."""

    def __init__(self, model: Model, tempdir: str):
        self.model: Model = model
        self.tempdir = tempdir

    def read_swap_csv(self, which: Literal["csv", "csv_tz"]) -> DataFrame:
        """Read the output csv file.

        Since there are only two types of output files (csv and csv_ts), we
        handle them in the same method.

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

    def read_swap_log(self, directory: Path) -> str:
        """Read the log file."""

        log_files = [f for f in Path(directory).glob("*.log") if f.name != "reruns.log"]

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
        """Read through the log file and catch warnings emitted by the SWAP executable."""
        lines = log.split("\n")
        warnings = [
            line for line in lines if line.strip().lower().startswith("warning")
        ]
        return warnings

    def read_swap_ascii(self):
        """Read all output files that are not in csv format as strings."""
        ascii_extensions = [
            ext
            for ext in self.model.generalsettings.extensions
            if ext not in ["csv", "csv_tz"]
        ]

        list_dir = os.listdir(self.tempdir)
        list_dir = [f for f in list_dir if f.endswith(tuple(ascii_extensions))]
        if list_dir:
            dict_files = {
                f.split(".")[1]: self.model.read_file(Path(self.tempdir, f))
                for f in list_dir
            }
        return dict_files


class Model(PySWAPBaseModel, FileMixin, ComplexSerializableMixin):
    """Main class that runs the SWAP model.

    Attributes:
        metadata (Any): Metadata of the model.
        generalsettings (Any): Simulation settings.
        meteorology (Any): Meteorological data.
        crop (Any): Crop data.
        fixedirrigation (Any): Fixed irrigation settings.
        soilmoisture (Any): Soil moisture data.
        surfaceflow (Any): Surface flow data.
        evaporation (Any): Evaporation data.
        soilprofile (Any): Soil profile data.
        snowandfrost (Optional[Any]): Snow and frost data.
            Default is `SnowAndFrost(swsnow=0, swfrost=0)`.
        richards (Optional[Any): Richards data.
        lateraldrainage (Any): Lateral drainage data.
        bottomboundary (Any): Bottom boundary data.
        heatflow (Optional[Any): Heat flow data.
        solutetransport (Optional[Any): Solute transport data.

    Methods:
        write_swp: Write the .swp input file.
        validate: Validate the model.
        run: Run the model.
    """

    _validate_on_run: bool = PrivateAttr(default=False)

    metadata: Metadata | None = None
    version: str = Field(exclude=True, default="base")
    generalsettings: GeneralSettings | None = None
    meteorology: Meteorology | None = None
    crop: Crop | None = None
    fixedirrigation: FixedIrrigation | None = FixedIrrigation(swirfix=0)
    soilmoisture: SoilMoisture | None = None
    surfaceflow: SurfaceFlow | None = None
    evaporation: Evaporation | None = None
    soilprofile: SoilProfile | None = None
    snowandfrost: SnowAndFrost | None = SnowAndFrost(swsnow=0, swfrost=0)
    richards: RichardsSettings | None = RichardsSettings(swkmean=1, swkimpl=0)
    lateraldrainage: Drainage | None = None
    bottomboundary: BottomBoundary | None = None
    heatflow: HeatFlow | None = HeatFlow(swhea=0)
    solutetransport: SoluteTransport | None = SoluteTransport(swsolu=0)

    @model_validator(mode="after")
    def validate_all_components(self):
        if not getattr(self, "_validate_on_run", False):
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
        try:
            self._validate_on_run = True
            self.model_validate(self, context={"_validate_on_run": True})
        finally:
            self._validate_on_run = False
            logger.info("Validation successful.")

    def write_swp(self, path: str | Path, **kwargs):
        """Write the .swp input file."""
        self.save_file(
            string=self.swp, path=path, fname="swap", extension="swp", **kwargs
        )

    @property
    def swp(self):
        """The content of the swp file.

        Looping over the dict() because when model_dump() is
        used, the nested models are automatically serialized.
        """
        return self.concat_nested_models(self)

    def run(self, path: str | Path, silence_warnings: bool = False):
        """Run the model using ModelRunner."""
        self.validate()
        return ModelRunner(self).run(path, silence_warnings)
