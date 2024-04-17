from .utils.basemodel import PySWAPBaseModel
from .utils.files import save_file, open_file
from typing import Optional, Any, List
from pathlib import Path
import shutil
import tempfile
import subprocess
import os
from importlib import resources
from pydantic import BaseModel, ConfigDict
from pandas import DataFrame, read_csv, to_datetime
from numpy import nan
from ..soilwater import SnowAndFrost
from .richards import RichardsSettings
from ..extras import HeatFlow, SoluteTransport


class Result(BaseModel):
    summary: Optional[str]
    output: Optional[DataFrame]
    vap: Optional[Any]
    log: Optional[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )


class Model(PySWAPBaseModel):

    metadata: Any
    simsettings: Any
    meteorology: Any
    crop: Any
    irrigation: Any
    soilmoisture: Any
    surfaceflow: Any
    evaporation: Any
    soilprofile: Any
    snowandfrost: Optional[Any] = SnowAndFrost(swsnow=0, swfrost=0)
    richards: Optional[Any] = RichardsSettings(swkmean=1, swkimpl=0)
    lateraldrainage: Any
    bottomboundary: Any
    heatflow: Optional[Any] = HeatFlow(swhea=0)
    solutetransport: Optional[Any] = SoluteTransport(swsolu=0)

    def concat_swp(self, save: bool = False, path: Optional[str] = None) -> str:
        string = ''
        for k, v in dict(self).items():
            if v is None:
                continue
            string += v.model_string()
        if save:
            save_file(string=string, extension='swp',
                      fname='swap', mode='w', path=path)
        return string

    @staticmethod
    def _copy_swap(tempdir: Path) -> None:
        # Use a context manager to ensure the temporary file is cleaned up
        with resources.path("pyswap.libs.swap420-linux", "swap420") as exec_path:
            shutil.copy(str(exec_path), str(tempdir))
        print('Copying executable into temporary directory...')

    @staticmethod
    def _run_exe(tempdir: Path) -> str:

        result = subprocess.run('./swap420',
                                stdout=subprocess.PIPE,
                                cwd=tempdir)

        return result.stdout.decode()

    @staticmethod
    def _read_log(tempdir: Path):
        log_file = os.path.join(tempdir, 'swap_swap.log')

        with open(log_file, 'r') as f:
            log_data = f.read()
            return log_data

    @staticmethod
    def _read_output(path: Path):
        df = read_csv(path, comment='*', index_col='DATETIME')
        df.index = to_datetime(df.index)

        return df

    @staticmethod
    def _read_vap(path: Path):
        df = read_csv(path, skiprows=11, encoding_errors='replace')
        df.columns = df.columns.str.strip()
        df.replace(r'^\s*$', nan, regex=True, inplace=True)
        return df

    def run(self):
        """Main function that runs the model.

        TODO: implement asynchronous function that would run the swap exe and then check once in a few seconds if the swap.log is there.
        If it is there, read it and check status. If status is error, exit the with/while clause.
        """

        with tempfile.TemporaryDirectory(dir=r'./') as tempdir:

            self._copy_swap(tempdir)
            print('Executable copied successfully!')

            print('Preparing SWP file...')
            self.concat_swp(save=True, path=tempdir)
            print('SWP file saved successfully!')
            self.meteorology.save_met(tempdir)
            print('Meteorology file saved successfully!')
            self.lateraldrainage.save_drainage(tempdir)
            print('Drainage file saved successfully!')
            self.crop.save_crop(tempdir)
            print('Crop file saved successfully!')
            # self.irrigation.make_irrigation(tempdir)
            # print('Irrigation file saved successfully!')

            print('Preparing to run the model...')
            # run the model
            self._run_exe(tempdir)
            # create a Result object
            print('Model run successfully!')
            # print the content of the temporary directory
            print('Files in temporary directory:')

            result = Result(
                summary=open_file(Path(tempdir, 'result.blc')),
                output=self._read_output(
                    Path(tempdir, 'result_output.csv')),
                vap=self._read_vap(Path(tempdir, 'result.vap')),
                log=self._read_log(tempdir)
            )

        return result
