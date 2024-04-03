from .metadata import Metadata
from .simsettings import SimSettings
from ..atmosphere.meteorology import Meteorology
from ..plant.crop import Crop
from ..soilwater.irrigation import Irrigation
from ..soilwater.drainage import Drainage
from ..soilwater.soilmoisture import SoilMoisture
from ..soilwater.surfaceflow import SurfaceFlow
from ..soilwater.evaporation import Evaporation
from ..soilwater.soilprofile import SoilProfile
from ..soilwater.snow import SnowAndFrost
from ..soilwater.richards import RichardsSettings
from ..core.boundary import LateralDrainage
from ..core.boundary import BottomBoundary
from .utils.basemodel import PySWAPBaseModel
from typing import Optional
from pathlib import Path
import shutil
import tempfile
import subprocess
import os


class Model(PySWAPBaseModel):

    metadata: Metadata
    simsettings: SimSettings
    meteorology: Meteorology
    crop: Crop
    irrigation: Irrigation
    soilmoisture: SoilMoisture
    surfaceflow: SurfaceFlow
    evaporation: Evaporation
    soilprofile: SoilProfile
    snowandfrost: SnowAndFrost
    richards: RichardsSettings
    lateraldrainage: LateralDrainage
    bottomboundary: BottomBoundary
    drainage: Optional[Drainage] = None

    def concat_swp(self, save: bool = False) -> str:
        string = ''
        for k, v in dict(self).items():
            print(k, v)
            string += v.model_string()

        if save:
            with open('swap.swp', 'w') as f:
                f.write(string)
        return string

    @staticmethod
    def _copy_swap(tempdir: Path) -> None:
        shutil.copy('../libs/swap.exe', tempdir)
        print('Copying executable into temporary directory...')

    @staticmethod
    def _run_exe(tempdir: Path) -> str:

        result = subprocess.run([os.path.join(tempdir, 'swap.exe')],
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

        with tempfile.TemporaryDirectory(dir=r'../') as tempdir:

            # copy the executable
            self._copy_swap(tempdir)
            # Prepare and save SWP file
            self.concat_swp(save=True)
            # Save accompanying files
            self.meteorology.save_met()
            self.drainage.make_dra()
            self.crop.save_crop()
            self.irrigation.make_irrigation()

            # run the model
            result = self._run_exe(tempdir)

            print(result)

            log_data = self._read_log(tempdir)

            print(log_data)
