from dataclasses import dataclass
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


@dataclass
class Model:

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
    drainage: Drainage | None = None

    def save(self):
        """Saves the model to a .json file."""
        pass

    def run():
        """Runs the model and saves the results.
        Added line of docstring,
        """
        pass
