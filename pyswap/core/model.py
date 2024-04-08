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
from pandas import DataFrame, read_csv


class Result(BaseModel):
    summary: Optional[str]
    output: Optional[DataFrame]
    log: Optional[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )

    def plot(self, variable: Optional[str | List[str]]):
        if variable is not None:
            self.output[variable].plot()
        else:
            self.output.plot()


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
    snowandfrost: Any
    richards: Any
    lateraldrainage: Any
    bottomboundary: Any
    heatflow: Any
    solutetransport: Any

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
        # print files in the temporary directory
        print('Files in temporary directory:')
        print(os.listdir(tempdir))
        executable = os.path.join(tempdir, 'swap420')
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

    def run(self):
        """Main function that runs the model.
        """

        with tempfile.TemporaryDirectory(dir=r'./') as tempdir:

            # copy the executable
            print('Copying executable into temporary directory...')
            self._copy_swap(tempdir)
            print('Executable copied successfully!')

            print('Preparing SWP file...')
            # Prepare and save SWP file
            self.concat_swp(save=True, path=tempdir)
            print('SWP file saved successfully!')
            # Save accompanying files
            print('Saving accompanying files...')
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
            result = Result(
                summary=open_file('./result.blc', 'ascii'),
                output=read_csv('./result_output.csv', comment='*'),
                log=self._read_log(tempdir)
            )

        return result
