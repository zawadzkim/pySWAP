"""Plotting functionality for pySWAP.

Plotting of results depends heavily on the application of the model. Therefore,
in this module, I only inclduded a few examples of how to plot results for
specific cases.

Modules:
    evapotranspiration: Functions for plotting evapotranspiration data.
    watercontent: Functions for plotting water content data as heat map.
"""

from pyswap.core.plot.evapotranspiration import evapotranspiration
from pyswap.core.plot.watercontent import water_content

__all__ = ["evapotranspiration", "water_content"]
