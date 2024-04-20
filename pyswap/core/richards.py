"""
richards.py contains the settings for the Richards' equation with some reasonable defaults included.

The module contains the following classes:
    - RichardsSettings: Holds the settings for the Richards' equation.
"""

from .utils.basemodel import PySWAPBaseModel
from typing import Literal


class RichardsSettings(PySWAPBaseModel):
    """Settings for the Richards' equation."""
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
