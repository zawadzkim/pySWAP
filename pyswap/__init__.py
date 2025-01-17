# ruff: noqa: F401
from pyswap import gis, components, model, testcase

# This will be better if called as `from pyswap.db import HDF5`, makes it clear
# where it is coming from
from pyswap.core import db, plot, io
from pyswap.core.importers import load_swp
from pyswap.log import _setup_logger, set_log_level

__all__ = ['components', "gis", "db", "plot", "model", "testcase", "io", "load_swp", "set_log_level"]


_setup_logger()
