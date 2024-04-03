"""Solute transport."""

from pyswap.core.utils.basemodel import PySWAPBaseModel
from pandas import DataFrame
from typing import Literal, Optional


class SoluteTransport(PySWAPBaseModel):

    swsolu: Literal[0, 1]
    cpre: Optional[float] = None
    cdrain: Optional[float] = None
    swbotbc: Optional[Literal[0, 1]] = None
    cseep: Optional[float] = None
    ddif: Optional[float] = None
    tscf: Optional[float] = None
    swsp: Optional[Literal[0, 1]] = None
    frexp: Optional[float] = None
    cref: Optional[float] = None
    swdc: Optional[Literal[0, 1]] = None
    gampar: Optional[float] = None
    rtheta: Optional[float] = None
    bexp: Optional[float] = None
    swbr: Optional[Literal[0, 1]] = None
    daquif: Optional[float] = None
    poros: Optional[float] = None
    kfsat: Optional[float] = None
    decsat: Optional[float] = None
    cdraini: Optional[float] = None
    cseeparrtb: Optional[DataFrame] = None
    inissoil: Optional[DataFrame] = None
    miscellaneous: Optional[DataFrame] = None
