"""
# Atmosphere subpackage

Meteorological settings and data for SWAP simulations.

Modules:
    metfile: meteorological data for SWAP simulations
    meteorology: meteorological settings for SWAP simulations
___________________________________________________________________________
"""

from .meteorology import Meteorology
from .metfile import MetFile, load_from_csv, load_from_knmi
from .tables import RAINFLUX
