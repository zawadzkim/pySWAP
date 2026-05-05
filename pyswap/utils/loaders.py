# ruff: noqa: SIM210
# mypy: disable-error-code="operator"
# The operator error was being raised on the method that was matching the
# dictionarties in _parse_ascii_file. This was not a priority to fix.

import re
from pathlib import Path
from typing import Literal as _Literal

from pyswap import Model
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
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.defaults import EXTENSION_SWITCHES
from pyswap.core.io.io_ascii import open_ascii
from pyswap.core.io.process_ascii import parse_ascii_file

__all__ = ["load_swp"]


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
    # params = _parse_ascii_file(path)
    swp = open_ascii(path)
    params = parse_ascii_file(swp)
    # from among the parameters parsed from the ascii file, pop the switches
    extension_switches = {
        key: params.pop(key) for key in EXTENSION_SWITCHES if key in params
    }
    # create the extension list with only those switches that are = 1. get rid of the "sw" prefix

    extension_list = [
        key[2:]
        for key, value in extension_switches.items()
        if isinstance(value, int | str) and int(value) == 1
    ]

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

    for value in model_setup.values():
        value.update(params, inplace=True)

    ml = Model(metadata=metadata, **model_setup)

    return ml


def load_dra(path: Path):
    dra = open_ascii(path)
    params = parse_ascii_file(dra)

    flux_objects_startwith = [
        "drares",
        "infres",
        "swallo",
        "l",
        "zbotdr",
        "swdtyp",
        "datowltb",
    ]

    flux_objects = {
        k: v
        for k, v in params.items()
        if any(re.match(f"{prefix}[1-5]$", k) for prefix in flux_objects_startwith)
    }
    other_params = {k: v for k, v in params.items() if k not in flux_objects}

    flux = Flux(**flux_objects)
    dra = DraFile(**other_params, fluxes=flux)

    return dra


def load_crp(path: Path, crptype: _Literal["fixed", "wofost", "grass"], name: str):
    crp = open_ascii(path)
    params = parse_ascii_file(crp, grass=True if crptype == "grass" else False)

    cropfile_setup = {
        "name": name,
        "prep": Preparation(),
        "cropdev_settings": CropDevelopmentSettingsFixed()
        if crptype == "fixed"
        else CropDevelopmentSettingsWOFOST()
        if crptype == "wofost"
        else CropDevelopmentSettingsGrass(),
        "oxygenstress": OxygenStress(),
        "droughtstress": DroughtStress(),
        "saltstress": SaltStress(),
        "compensaterwu": CompensateRWUStress(),
        "interception": Interception(),
        "scheduledirrigation": ScheduledIrrigation(),
        "grasslandmanagement": GrasslandManagement(),
        "co2correction": CO2Correction(),
    }

    for value in cropfile_setup.values():
        if isinstance(value, str):
            continue
        if isinstance(value, PySWAPBaseModel):
            value.update(new=params, inplace=True)
        else:
            continue

    crp = CropFile(**cropfile_setup)

    return crp


def load_bbc(path: Path, bottomboundary: BottomBoundary | None = None):
    """Load the bottom boundary conditions from a .bbc file.

    Bottom boundary conditions are stored in the same class. Therefore this
    function can either return a new instance of the class or update an existing
    one.
    """
    bbc = open_ascii(path)
    params = parse_ascii_file(bbc)

    if bottomboundary is None:
        bottomboundary = BottomBoundary()

    botbound = bottomboundary.update(params)

    return botbound
