"""SWAP model components.

This module contains the components of the pySWAP model. Each component is
implemented as a class that inherits from Pydantic BaseModel. The components
are used to store the input data for the model and to provide methods to
convert the data to the format required by the SWAP model.

The component classes, and the helpers that build a meteorological file, are
available directly from this package, e.g. `pyswap.components.Meteorology`.
They stay importable from their submodules (`pyswap.components.meteorology`,
...), which also hold the table schemas (e.g. `pyswap.components.crop.GCTB`).
"""

from pyswap.components import (
    boundary,
    crop,
    drainage,
    irrigation,
    meteorology,
    simsettings,
    soilwater,
    transport,
)
from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import (
    CO2Correction,
    CompensateRWUStress,
    Crop,
    CropDevelopmentSettingsFixed,
    CropDevelopmentSettingsGrass,
    CropDevelopmentSettingsWOFOST,
    CropFile,
    DroughtStress,
    GrasslandManagement,
    Interception,
    OxygenStress,
    Preparation,
    SaltStress,
)
from pyswap.components.drainage import DraFile, Drainage, Flux
from pyswap.components.irrigation import FixedIrrigation, ScheduledIrrigation
from pyswap.components.metadata import Metadata
from pyswap.components.meteorology import (
    Meteorology,
    MetFile,
    metfile_from_csv,
    metfile_from_knmi,
)
from pyswap.components.simsettings import GeneralSettings, RichardsSettings
from pyswap.components.soilwater import (
    Evaporation,
    SnowAndFrost,
    SoilMoisture,
    SoilProfile,
    SurfaceFlow,
)
from pyswap.components.transport import HeatFlow, SoluteTransport

__all__ = [
    "BottomBoundary",
    "CO2Correction",
    "CompensateRWUStress",
    "Crop",
    "CropDevelopmentSettingsFixed",
    "CropDevelopmentSettingsGrass",
    "CropDevelopmentSettingsWOFOST",
    "CropFile",
    "DraFile",
    "Drainage",
    "DroughtStress",
    "Evaporation",
    "FixedIrrigation",
    "Flux",
    "GeneralSettings",
    "GrasslandManagement",
    "HeatFlow",
    "Interception",
    "MetFile",
    "Metadata",
    "Meteorology",
    "OxygenStress",
    "Preparation",
    "RichardsSettings",
    "SaltStress",
    "ScheduledIrrigation",
    "SnowAndFrost",
    "SoilMoisture",
    "SoilProfile",
    "SoluteTransport",
    "SurfaceFlow",
    "boundary",
    "crop",
    "drainage",
    "irrigation",
    "metadata",
    "meteorology",
    "metfile_from_csv",
    "metfile_from_knmi",
    "simsettings",
    "soilwater",
    "transport",
]
