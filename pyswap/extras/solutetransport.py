"""Solute transport."""

from dataclasses import dataclass
from pyswap.core.dtypes import Subsection
from pandas import DataFrame


@dataclass
class SoluteTransport(Subsection):

    swsolu: bool
    cpre: float | None = None
    cdrain: float | None = None
    swbotbc: int | None = None
    cseep: float | None = None
    ddif: float | None = None
    tscf: float | None = None
    swsp: bool | None = None
    frexp: float | None = None
    cref: float | None = None
    swdc: bool | None = None
    gampar: float | None = None
    rtheta: float | None = None
    bexp: float | None = None
    swbr: bool | None = None
    daquif: float | None = None
    poros: float | None = None
    kfsat: float | None = None
    decsat: float | None = None
    cdraini: float | None = None
    cseeparrtb: DataFrame | None = None
    inissoil: DataFrame | None = None
    miscellaneous: DataFrame | None = None
