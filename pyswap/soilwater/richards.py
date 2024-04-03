from dataclasses import dataclass, field
from ..core.utils.basemodel import Section, Subsection, PySWAPBaseModel
from pandas import DataFrame


class RichardsSettings(PySWAPBaseModel):
    swkmean: int
    swkimpl: bool
    dtmin: float = 1e-06
    dtmax: float = 0.04
    gwlconv: float = 100.0
    critdevh1cp: float = 0.01
    critdevh2cp: float = 0.1
    critdevponddt: float = 0.0001
    maxit: int = 30
    maxbacktr: int = 3
