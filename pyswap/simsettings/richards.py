"""
Settings for the Richards' equation with some reasonable defaults included.

Classes:
    RichardsSettings: Holds the settings for the Richards' equation.
"""

from ..core import PySWAPBaseModel
from typing import Literal


class RichardsSettings(PySWAPBaseModel):
    """Settings for the Richards' equation.

    Attributes:
        swkmean (int): Switch for averaging method of hydraulic conductivity
        swkimpl (Literal[0, 1]): Switch for updating hydraulic conductivity during iteration
        dtmin (float): Minimum timestep
        dtmax (float): Maximum timestep
        gwlconv (float): Maximum difference of groundwater level between time steps
        critdevh1cp (float): Maximum relative difference in pressure heads per compartment
        critdevh2cp (float): Maximum absolute difference in pressure heads per compartment
        critdevponddt (float): Maximum water balance error of ponding layer
        maxit (int): Maximum number of iteration cycles
        maxbacktr (int): Maximum number of back track cycles within an iteration cycle
    """

    swkmean: int
    swkimpl: Literal[0, 1]
    dtmin: float = 0.000001
    dtmax: float = 0.04
    gwlconv: float = 100.0
    critdevh1cp: float = 0.01
    critdevh2cp: float = 0.1
    critdevponddt: float = 0.0001
    maxit: int = 30
    maxbacktr: int = 3
