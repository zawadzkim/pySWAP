import logging

# For the direct access on the package level
from pyswap.components import *
from pyswap.gis import *
from pyswap.model import *
from pyswap.core.db import *

# for the __all__ variable
from pyswap import components, gis, model
from pyswap.core import db


__all__ = [
    *components.__all__,
    *gis.__all__,
    *model.__all__,
    *db.__all__,
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
