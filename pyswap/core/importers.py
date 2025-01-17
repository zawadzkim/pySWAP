from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import Crop
from pyswap.components.drainage import Drainage
from pyswap.components.irrigation import FixedIrrigation
from pyswap.components.meteorology import Meteorology
from pyswap.components.simsettings import GeneralSettings, RichardsSettings
from pyswap.components.soilwater import Evaporation, SnowAndFrost, SoilMoisture, SoilProfile, SurfaceFlow
from pyswap.components.transport import HeatFlow, SoluteTransport
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.io.io_ascii import open_ascii
from pyswap.core.io.old_swap import create_schema_object, parse_ascii_file, remove_comments
from pyswap.model import Model


from pathlib import Path

__all__ = ["load_swp"]

def load_swp(path: Path, metadata: PySWAPBaseModel) -> PySWAPBaseModel:
    """Load a SWAP model from a .swp file.

    Parameters:
        path (Path): Path to the .swp file.

    Returns:
        PySWAPBaseModel: The loaded model.
    """
    swp = open_ascii(path)
    text = remove_comments(swp)
    pairs, tables = parse_ascii_file(text)
    schema_objects = create_schema_object(tables)

    # pairs = {k: (int(v) if k.startswith("sw") else v) for k, v in pairs.items()}

    params = pairs | schema_objects

    for k, v in params.items():
        print(k, "=", v)
    # model definition
    model_setup = {
        "generalsettings": GeneralSettings(),
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