"""Heat flow"""
from dataclasses import dataclass
from pyswap.core.dtypes import Subsection
from pandas import DataFrame


@dataclass
class HeatFlow(Subsection):

    swhea: bool
    swcalt: int | None = None
    tampli: float | None = None
    tmean: float | None = None
    timref: float | None = None
    ddamp: float | None = None
    swtopbhea: int | None = None
    tsoilfile: str | None = None
    swbotbhea: int | None = None
    soiltextures: DataFrame | None = None
    initsoil: DataFrame | None = None
    bbctsoil: DataFrame | None = None
