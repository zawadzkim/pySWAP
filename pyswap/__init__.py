# ruff: noqa: F401
from pyswap import gis, components, testcase
from pyswap.model import Model, run_parallel

# This will be better if called as `from pyswap.db import HDF5`, makes it clear
# where it is coming from
from pyswap.core import db, plot, io
from pyswap.core.loaders import load_swp
from pyswap.log import _setup_logger, set_log_level

__all__ = ['components', "gis", "db", "plot", "testcase", "io", "load_swp", "set_log_level", "Model", "run_parallel"]


_setup_logger()
