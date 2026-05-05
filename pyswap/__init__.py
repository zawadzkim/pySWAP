# Version information
import importlib.metadata
import logging

from pyswap import components, db, gis, testcase

# # This will be better if called as `from pyswap.db import HDF5`, makes it clear
# # where it is coming from
from pyswap.core import io, plot
from pyswap.log import set_log_level, setup_logging
from pyswap.model.model import Model, run_parallel
from pyswap.utils.executables import check_swap, get_swap, show_info
from pyswap.utils.loaders import load_bbc, load_crp, load_dra, load_swp

__version__ = importlib.metadata.version("pyswap")

__all__ = [
    "Model",
    "check_swap",
    "components",
    "db",
    "get_swap",
    "gis",
    "io",
    "load_bbc",
    "load_crp",
    "load_dra",
    "load_swp",
    "plot",
    "run_parallel",
    "set_log_level",
    "setup_logging",
    "show_info",
    "testcase",
]


logging.getLogger("pyswap").addHandler(logging.NullHandler())
