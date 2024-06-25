"""Solute transport settings for the SWAP simulation.

Classes:
    SoluteTransport: Solute transport settings.
"""

from ..core import PySWAPBaseModel
from ..core import Table
from typing import Literal, Optional
from typing_extensions import Self


class SoluteTransport(PySWAPBaseModel):
    """
    Solute transport settings.

    !!! warning

        Validation not yet included in the current release.

    Attributes:
        swsolu (Literal[0, 1]): 
        cpre (Optional[float]):
        cdrain (Optional[float]):
        swbotbc (Optional[Literal[0, 1]]):
        cseep (Optional[float]):
        ddif (Optional[float]):
        tscf (Optional[float]):
        swsp (Optional[Literal[0, 1]]):
        frexp (Optional[float]):
        cref (Optional[float]):
        swdc (Optional[Literal[0, 1]]):
        gampar (Optional[float]):
        rtheta (Optional[float]):
        bexp (Optional[float]):
        swbr (Optional[Literal[0, 1]]):
        daquif (Optional[float]):
        poros (Optional[float]):
        kfsat (Optional[float]):
        decsat (Optional[float]):
        cdraini (Optional[float]):
        table_cseeparrtb (Optional[Table]):
        table_inissoil (Optional[Table]):
        table_miscellaneous (Optional[Table]):
    """
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
    table_cseeparrtb: Optional[Table] = None
    table_inissoil: Optional[Table] = None
    table_miscellaneous: Optional[Table] = None
