from dataclasses import dataclass, field
from ..core.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class RichardsSettings(Subsection):
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
