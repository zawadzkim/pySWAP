"""The main model class.

Classes:
    Model: Main class that runs the SWAP model.
"""

import logging
import os
import shutil
import subprocess
import tempfile
import warnings
from importlib import resources
from pathlib import Path

from pandas import read_csv, to_datetime
from pydantic import Field

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


class Model(PySWAPBaseModel, FileMixin, ComplexSerializableMixin):
    """Main class that runs the SWAP model.

    Attributes:
        metadata (Any): Metadata of the model.
        general_settings (Any): Simulation settings.
        meteorology (Any): Meteorological data.
        crop (Any): Crop data.
        fixedirrigation (Any): Fixed irrigation settings.
        soilmoisture (Any): Soil moisture data.
        surfaceflow (Any): Surface flow data.
        evaporation (Any): Evaporation data.
        soilprofile (Any): Soil profile data.
        snowandfrost (Optional[Any]): Snow and frost data.
            Default is `SnowAndFrost(swsnow=0, swfrost=0)`.
        richards (Optional[Any]): Richards data.
        lateraldrainage (Any): Lateral drainage data.
        bottomboundary (Any): Bottom boundary data.
        heatflow (Optional[Any]): Heat flow data.
        solutetransport (Optional[Any]): Solute transport data.

    Methods:
        write_swp: Write the .swp input file.
        _copy_executable: Copy the appropriate SWAP executable to
            the temporary directory.
        _run_swap: Run the SWAP executable.
        _read_output: Read the output file.
        _read_output_tz: Read the output file with time zone.
        _read_vap: Read the .vap output file.
        _write_inputs: Write the input files.
        _identify_warnings: Identify warnings in the log file.
        _raise_swap_warning: Raise a warning.
        _read_output_old: Save the old output files.
        run: Run the model.
    """

    metadata: Metadata
    version: str = Field(exclude=True, default="base")
    general_settings: GeneralSettings
    meteorology: Meteorology
    crop: Crop
    fixedirrigation: FixedIrrigation = FixedIrrigation(swirfix=0)
    soilmoisture: SoilMoisture
    surfaceflow: SurfaceFlow
    evaporation: Evaporation
    soilprofile: SoilProfile
    snowandfrost: SnowAndFrost | None = SnowAndFrost(swsnow=0, swfrost=0)
    richards: RichardsSettings | None = RichardsSettings(swkmean=1, swkimpl=0)
    lateraldrainage: Drainage
    bottomboundary: BottomBoundary
    heatflow: HeatFlow | None = HeatFlow(swhea=0)
    solutetransport: SoluteTransport | None = SoluteTransport(swsolu=0)

    @property
    def swp(self):
        """The content of the swp file.

        Looping over the dict() because when model_dump() is
        used, the nested models are automatically serialized.
        """

        return self.concat_nested_models(self)

    def _write_swp(self, path: str) -> None:
        """Write the .swp input file."""

        self.save_file(string=self.swp, path=path, fname="swap", extension="swp")

    @staticmethod
    def _copy_executable(tempdir: Path):
        """Copy the appropriate SWAP executable to
        the temporary directory."""
        if IS_WINDOWS:
            exec_path = resources.files("pyswap.libs.swap420-exe").joinpath("swap.exe")
            shutil.copy(str(exec_path), str(tempdir))
            print("Copying the windows version of SWAP into temporary directory...")
        else:
            exec_path = resources.files("pyswap.libs.swap420-linux").joinpath("swap420")
            shutil.copy(str(exec_path), str(tempdir))
            print("Copying linux executable into temporary directory...")

    def _write_inputs(self, path: str) -> None:
        print("Preparing files...")
        self._write_swp(path)
        if self.lateraldrainage.drafile:
            self.lateraldrainage.write_dra(path)
        if self.crop.cropfiles:
            self.crop.write_crop(path)
        if self.meteorology.metfile:
            self.meteorology.write_met(path)
        if self.fixedirrigation.irgfile:
            self.irrigation.fixedirrig.write_irg(path)
        if self.bottomboundary.swbbcfile:
            self.bottomboundary.write_bbc(path)

    @staticmethod
    def _run_swap(tempdir: Path) -> str:
        """Run the SWAP executable.

        I do not decode the sterror because the SWAP executable
        writes errors to stdout. It will be easy to implement reading
        stderr later if needed.

        Returns:
            str: stdout.
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

    @staticmethod
    def _read_output(path: Path):
        """Read the output csv file."""
        df = read_csv(path, comment="*", index_col="DATETIME")
        df.index = to_datetime(df.index)

        return df

    @staticmethod
    def _read_output_tz(path: Path):
        """Read the output csv file with the depth information."""
        df = read_csv(path, comment="*", index_col="DATE")
        df.index = to_datetime(df.index)

        return df

    def _read_log_file(self, directory: Path) -> str:
        """Read the log file."""
        # log_files = [f for f in Path(directory).glob(
        #     '*.log') if f.name != 'reruns.log']
        log_files = [f for f in Path(directory).glob("*.log") if f.name != "reruns.log"]
        if len(log_files) == 0:
            raise FileNotFoundError("No .log file found in the directory.")
        elif len(log_files) > 1:
            raise FileExistsError("Multiple .log files found in the directory.")

        log_file = log_files[0]

        with open(log_file) as file:
            log_content = file.read()

        return log_content

    @staticmethod
    def _identify_warnings(log: str) -> list[Warning]:
        """Read through the log file and catch warnings emitted by
        the SWAP executable."""
        lines = log.split("\n")
        warnings = [
            line for line in lines if line.strip().lower().startswith("warning")
        ]

        return warnings

    def _raise_swap_warning(self, message):
        warnings.warn(message, Warning, stacklevel=3)

    def _read_output_old(self, tempdir: Path):
        """Read all output files that are not in csv format as strings."""
        list_dir = os.listdir(tempdir)
        list_dir = [
            f
            for f in list_dir
            if not f.find(self.general_settings.outfil) and not f.endswith(".csv")
        ]

        if list_dir:
            dict_files = {
                f.split(".")[1]: self.read_file(Path(tempdir, f)) for f in list_dir
            }
        return dict_files

    def run(
        self, path: str | Path, silence_warnings: bool = False, old_output: bool = False
    ):
        """Main function that runs the model.

        Parameters:
            path (str): Path to the working directory.
            silence_warnings (bool): If True, warnings will not be printed.
            old_output (bool): If True, the old output files (like .vap) will
            be saved to a dictionary.


        !!! warning

            Reruns are for now not supported. Multiple runs of the model can
            be achieved by running model.run() multiple times.
        """
        with tempfile.TemporaryDirectory(dir=path) as tempdir:
            self._copy_executable(tempdir)
            self._write_inputs(tempdir)

            result = self._run_swap(tempdir)

            if "normal completion" not in result:
                raise Exception(f"Model run failed. \n {result}")

            print(result)

            log = self._read_log_file(tempdir)
            warnings = self._identify_warnings(log)

            if warnings and not silence_warnings:
                print("Warnings:")
                for warning in warnings:
                    self._raise_swap_warning(message=warning)

            if old_output:
                dict_files = self._read_output_old(tempdir)

            result = Result(
                output=self._read_output(
                    Path(tempdir, f"{self.general_settings.outfil}_output.csv")
                )
                if self.general_settings.inlist_csv
                else None,
                output_tz=self._read_output_tz(
                    Path(tempdir, f"{self.general_settings.outfil}_output_tz.csv")
                )
                if self.general_settings.inlist_csv_tz
                else None,
                log=log,
                output_old=dict_files if old_output else None,
                warning=warnings,
            )

            return result
