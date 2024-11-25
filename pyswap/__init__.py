from .simsettings import Metadata, GeneralSettings, RichardsSettings, MeteoLocation, ModelLocation
from .atmosphere import Meteorology, MetFile
from .boundary import BBCFile, BottomBoundary
from .core.database import HDF5
from .drainage import (
    DraFile,
    Drainage,
    DrainageFluxTable,
    DrainageFormula,
    DrainageInfRes,
    DraSettings,
    Flux,
)
from .extras import HeatFlow, SoluteTransport
from .irrigation import FixedIrrigation, IrgFile, ScheduledIrrigation
from .model import Model, Result
from .plant import (
    CO2Correction,
    CompensateRWUStress,
    Crop,
    CropDevelopmentSettings,
    CropDevelopmentSettingsFixed,
    CropDevelopmentSettingsWOFOST,
    CropFile,
    DroughtStress,
    GrasslandManagement,
    Interception,
    OxygenStress,
    Preparation,
    SaltStress,
)
from .simsettings import GeneralSettings, Metadata, RichardsSettings
from .soilwater import Evaporation, SnowAndFrost, SoilMoisture, SoilProfile, SurfaceFlow
from .gis.location import Location
import logging
from .libs import all_paths

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
