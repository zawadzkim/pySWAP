# ruff: noqa: F401
# Version information
import importlib.metadata
import logging

from pyswap import components, db, gis, testcase

# # This will be better if called as `from pyswap.db import HDF5`, makes it clear
# # where it is coming from
from pyswap.core import io, plot
from pyswap.log import setup_logging, set_log_level
from pyswap.model.model import Model, run_parallel
from pyswap.utils.executables import check_swap, get_swap, show_info
from pyswap.utils.loaders import load_bbc, load_crp, load_dra, load_swp

__version__ = importlib.metadata.version("pyswap")

__all__ = [
    "components",
    "gis",
    "db",
    "plot",
    "testcase",
    "io",
    "load_swp",
    "load_dra",
    "load_crp",
    "load_bbc",
    "set_log_level",
    "setup_logging",
    "Model",
    "run_parallel",
    "get_swap",
    "check_swap",
    "show_info",
]


logging.getLogger("pyswap").addHandler(logging.NullHandler())
