"""The main model class.

Classes:
    Model: Main class that runs the SWAP model.
"""

from ..core import PySWAPBaseModel
from ..core import open_file
from typing import Optional, Any
from pathlib import Path
import shutil
import tempfile
import subprocess
import os
from importlib import resources
from pandas import read_csv, to_datetime
from numpy import nan
from ..extras import HeatFlow, SoluteTransport
from ..atmosphere import Meteorology
from ..irrigation import FixedIrrigation
from ..soilwater import SoilMoisture, SnowAndFrost, Evaporation, SoilProfile, SurfaceFlow
from ..simsettings import Metadata, GeneralSettings, RichardsSettings
from ..boundary import BottomBoundary
from ..drainage import Drainage
from ..plant import Crop
from .result import Result
import warnings
import platform
from pydantic import Field

IS_WINDOWS = platform.system() == 'Windows'


class Model(PySWAPBaseModel):
    """Main class that runs the SWAP model.

    The attributes must be valid pySWAP classes. For avoiding validation errors,
    for now the attributes are defined as Any.

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
        snowandfrost (Optional[Any]): Snow and frost data. Default is `SnowAndFrost(swsnow=0, swfrost=0)`.
        richards (Optional[Any]): Richards data.
        lateraldrainage (Any): Lateral drainage data.
        bottomboundary (Any): Bottom boundary data.
        heatflow (Optional[Any]): Heat flow data.
        solutetransport (Optional[Any]): Solute transport data.

    Methods:
        write_swp: Write the .swp input file.
        _copy_executable: Copy the appropriate SWAP executable to the temporary directory.
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
    version: str = Field(exclude=True, default='base')
    general_settings: GeneralSettings
    meteorology: Meteorology
    crop: Crop
    fixedirrigation: FixedIrrigation = FixedIrrigation(swirfix=0)
    soilmoisture: SoilMoisture
    surfaceflow: SurfaceFlow
    evaporation: Evaporation
    soilprofile: SoilProfile
    snowandfrost: Optional[SnowAndFrost] = SnowAndFrost(swsnow=0, swfrost=0)
    richards: Optional[RichardsSettings] = RichardsSettings(
        swkmean=1, swkimpl=0)
    lateraldrainage: Drainage
    bottomboundary: BottomBoundary
    heatflow: Optional[HeatFlow] = HeatFlow(swhea=0)
    solutetransport: Optional[SoluteTransport] = SoluteTransport(swsolu=0)

    def write_swp(self, path: str) -> None:
        """Write the .swp input file."""

        string = self._concat_sections()
        self.save_element(string=string, path=path,
                          filename='swap', extension='swp')
        print('swap.swp saved.')

    @staticmethod
    def _copy_executable(tempdir: Path):
        """Copy the appropriate SWAP executable to the temporary directory."""
        if IS_WINDOWS:
            exec_path = resources.files(
                "pyswap.libs.swap420-exe").joinpath("swap.exe")
            shutil.copy(str(exec_path), str(tempdir))
            print('Copying the windows version of SWAP into temporary directory...')
        else:
            exec_path = resources.files(
                "pyswap.libs.swap420-linux").joinpath("swap420")
            shutil.copy(str(exec_path), str(tempdir))
            print('Copying linux executable into temporary directory...')

    def _write_inputs(self, path: str) -> None:
        print('Preparing files...')
        self.write_swp(path)
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

        swap_path = Path(tempdir, 'swap.exe') if IS_WINDOWS else './swap420'

        p = subprocess.Popen(swap_path,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=tempdir)

        stdout = p.communicate(input=b'\n')[0]

        return stdout.decode()

    @staticmethod
    def _read_output(path: Path):
        """Read the output csv file."""
        df = read_csv(path, comment='*', index_col='DATETIME')
        df.index = to_datetime(df.index)

        return df

    @staticmethod
    def _read_output_tz(path: Path):
        """Read the output csv file with the depth information."""
        df = read_csv(path, comment='*', index_col='DATE')
        df.index = to_datetime(df.index)

        return df

    @staticmethod
    def _read_vap(path: Path):
        df = read_csv(path, skiprows=11, encoding_errors='replace')
        df.columns = df.columns.str.strip()
        df.replace(r'^\s*$', nan, regex=True, inplace=True)
        return df

    def _read_log_file(self, directory: Path) -> str:
        """Read the log file."""
        log_files = [f for f in Path(directory).glob(
            '*.log') if f.name != 'reruns.log']

        if len(log_files) == 0:
            raise FileNotFoundError("No .log file found in the directory.")
        elif len(log_files) > 1:
            raise FileExistsError(
                "Multiple .log files found in the directory.")

        log_file = log_files[0]

        with open(log_file, 'r') as file:
            log_content = file.read()

        return log_content

    @staticmethod
    def _identify_warnings(log: str) -> list[Warning]:
        """Read through the log file and catch warnings emitted by the SWAP executable."""
        lines = log.split('\n')
        warnings = [line for line in lines
                    if line.strip().lower().startswith('warning')]

        return warnings

    def _raise_swap_warning(self, message):
        warnings.warn(message, Warning, stacklevel=3)

    def _read_output_old(self, tempdir: Path):
        """Read all output files that are not in csv format as strings."""
        list_dir = os.listdir(tempdir)
        list_dir = [f for f in list_dir if not f.find(
            self.general_settings.outfil) and not f.endswith('.csv')]

        if list_dir:
            dict_files = {f.split('.')[1]: open_file(Path(tempdir, f))
                          for f in list_dir}

        return dict_files

    def run(self, path: str | Path, silence_warnings: bool = False, old_output: bool = False):
        """Main function that runs the model.

        Parameters:
            path (str): Path to the working directory.
            silence_warnings (bool): If True, warnings will not be printed.
            old_output (bool): If True, the old output files (like .vap) will be saved to a dictionary.

        !!! todo

            It would be nice to have a nice output string that will concatenate all output
            including warnings and/or errors.


        !!! warning

            Reruns are for now not supported. Multiple runs of the model can be achieved by running
            model.run() multiple times.
        """
        with tempfile.TemporaryDirectory(dir=path) as tempdir:

            self._copy_executable(tempdir)
            self._write_inputs(tempdir)

            result = self._run_swap(tempdir)

            if 'normal completion' not in result:
                raise Exception(
                    f'Model run failed. \n {result}')

            print(result)

            log = self._read_log_file(tempdir)
            warnings = self._identify_warnings(log)

            if warnings and not silence_warnings:
                print('Warnings:')
                for warning in warnings:
                    self._raise_swap_warning(message=warning)

            if old_output:
                dict_files = self._read_output_old(tempdir)

            result = Result(
                output=self._read_output(
                    Path(tempdir, f'{self.general_settings.outfil}_output.csv')) if self.general_settings.inlist_csv else None,
                output_tz=self._read_output_tz(
                    Path(tempdir, f'{self.general_settings.outfil}_output_tz.csv')) if self.general_settings.inlist_csv_tz else None,
                log=log,
                output_old=dict_files if old_output else None,
                warning=warnings
            )

            return result
