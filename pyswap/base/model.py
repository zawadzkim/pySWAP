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
from ..base.boundary import LateralDrainage
from ..base.boundary import BottomBoundary


@dataclass
class Model:

    metadata: Metadata
    simsettings: SimSettings
    meteorology: Meteorology
    crop: Crop
    irrigation: Irrigation
    drainage: Drainage
    soilmoisture: SoilMoisture
    surfaceflow: SurfaceFlow
    evaporation: Evaporation
    soilprofile: SoilProfile
    snowandfrost: SnowAndFrost
    richards: RichardsSettings
    lateraldrainage: LateralDrainage
    bottomboundary: BottomBoundary
