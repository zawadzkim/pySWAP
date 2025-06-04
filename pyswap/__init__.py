# ruff: noqa: F401
from pyswap import components, db, gis, testcase

# # This will be better if called as `from pyswap.db import HDF5`, makes it clear
# # where it is coming from
from pyswap.core import io, plot
from pyswap.log import _setup_logger, set_log_level
from pyswap.model.model import Model, run_parallel
from pyswap.utils.loaders import load_bbc, load_crp, load_dra, load_swp

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
    "Model",
    "run_parallel",
]


_setup_logger()
