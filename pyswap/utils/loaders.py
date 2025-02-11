from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import Crop
from pyswap.components.drainage import Drainage
from pyswap.components.irrigation import ScheduledIrrigation, FixedIrrigation
from pyswap.components.meteorology import Meteorology
from pyswap.components.simsettings import GeneralSettings, RichardsSettings
from pyswap.components.soilwater import Evaporation, SnowAndFrost, SoilMoisture, SoilProfile, SurfaceFlow
from pyswap.components.transport import HeatFlow, SoluteTransport
from pyswap.components.drainage import Flux, DraFile
from pyswap.components.crop import CropFile, CropDevelopmentSettingsWOFOST, CropDevelopmentSettingsFixed, CropDevelopmentSettingsGrass, OxygenStress, DroughtStress, SaltStress, CompensateRWUStress, Interception, CO2Correction, Preparation, GrasslandManagement

from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.io.io_ascii import open_ascii
from pyswap.core.io.old_swap import create_table_objects, create_array_objects, parse_ascii_file, remove_comments
from pyswap.model import Model
from pyswap.core.defaults import EXTENSION_SWITCHES

from typing import Literal as _Literal
import re
from pathlib import Path

__all__ = ["load_swp"]


def _parse_ascii_file(path: Path, grass_crp: bool = False):
    """Parse the .swp file and return the parameters."""
    swp = open_ascii(path)
    text = remove_comments(swp)
    pairs, arrays, tables = parse_ascii_file(text)
    table_objects = create_table_objects(tables)
    array_objects = create_array_objects(arrays, grass_crp)

    params = pairs | table_objects | array_objects

    return params

def load_swp(path: Path, metadata: PySWAPBaseModel) -> Model:
    """Load a SWAP model from a .swp file.

    Parameters:
        path (Path): Path to the .swp file.

    Returns:
        PySWAPBaseModel: The loaded model.
    """
    # finish this one up. Essentialle you need to pop the extension switches
    # from the main dictionary and then create the extension list. The names
    # have to be handled properly.
    params = _parse_ascii_file(path)
    # from among the parameters parsed from the ascii file, pop the switches
    extension_switches = {key: params.pop(key) for key in EXTENSION_SWITCHES if key in params}
    # create the extension list with only those switches that are = 1. get rid of the "sw" prefix

    extension_list = [key[2:] for key, value in extension_switches.items() if int(value) == 1]

    # model definition
    model_setup = {
        "generalsettings": GeneralSettings(extensions=extension_list),
        "meteorology": Meteorology(),
        "crop": Crop(),
        "fixedirrigation": FixedIrrigation(),
        "soilmoisture": SoilMoisture(),
        "surfaceflow": SurfaceFlow(),
        "evaporation": Evaporation(),
        "soilprofile": SoilProfile(),
        "snowandfrost": SnowAndFrost(),
        "richards": RichardsSettings(),
        "lateraldrainage": Drainage(),
        "bottomboundary": BottomBoundary(),
        "heatflow": HeatFlow(),
        "solutetransport": SoluteTransport(),
    }

    for key, value in model_setup.items():
        value.update(params, inplace=True)

    ml = Model(metadata=metadata, **model_setup)

    return ml

def load_dra(path: Path):
    params = _parse_ascii_file(path)

    flux_objects_startwith = [
        "drares",
        "infres",
        "swallo",
        "l",
        "zbotdr",
        "swdtyp",
        "datowltb",
    ]

    flux_objects = {k: v for k, v in params.items() if any(re.match(f"{prefix}[1-5]$", k) for prefix in flux_objects_startwith)}
    other_params = {k: v for k, v in params.items() if k not in flux_objects}
    
    flux = Flux(**flux_objects)
    dra = DraFile(**other_params, fluxes=flux)

    return dra


def load_crp(path: Path, type: _Literal["fixed", "wofost", "grass"], name: str):
    params = _parse_ascii_file(path, grass_crp=True if type == "grass" else False)

    cropfile_setup = {
        "name": name,
        "prep": Preparation(),
        "cropdev_settings": CropDevelopmentSettingsFixed() if type == "fixed" else CropDevelopmentSettingsWOFOST() if type == "wofost" else CropDevelopmentSettingsGrass(),
        "oxygenstress": OxygenStress(),
        "droughtstress": DroughtStress(),
        "saltstress": SaltStress(),
        "compensaterwu": CompensateRWUStress(),
        "interception": Interception(),
        "scheduledirrigation": ScheduledIrrigation(),
        "grasslandmanagement": GrasslandManagement(),
        "co2correction": CO2Correction(),
    }

    for key, value in cropfile_setup.items():
        if isinstance(value, str):
            continue
        value.update(new=params, inplace=True)

    crp = CropFile(**cropfile_setup)

    return crp

def load_bbc(path: Path, bottomboundary: BottomBoundary | None = None):
    """Load the bottom boundary conditions from a .bbc file.
    
    Bottom boundary conditions are stored in the same class. Therefore this
    function can either return a new instance of the class or update an existing
    one.
    """
    params = _parse_ascii_file(path)

    if bottomboundary is None:
        bottomboundary = BottomBoundary()

    botbound = bottomboundary.update(params)
    
    return botbound
    