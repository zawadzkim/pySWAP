"""Solute transport settings for the SWAP simulation.

Classes:
    SoluteTransport: Solute transport settings.
"""

from typing import Literal

from ..core import PySWAPBaseModel, SerializableMixin, Table
from ..core.mixins import YAMLValidatorMixin


class SoluteTransport(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """
    Solute transport settings.

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
    cpre: float | None = None
    cdrain: float | None = None
    swbotbc: Literal[0, 1] | None = None
    cseep: float | None = None
    ddif: float | None = None
    tscf: float | None = None
    swsp: Literal[0, 1] | None = None
    frexp: float | None = None
    cref: float | None = None
    swdc: Literal[0, 1] | None = None
    gampar: float | None = None
    rtheta: float | None = None
    bexp: float | None = None
    swbr: Literal[0, 1] | None = None
    daquif: float | None = None
    poros: float | None = None
    kfsat: float | None = None
    decsat: float | None = None
    cdraini: float | None = None
    table_cseeparrtb: Table | None = None
    table_inissoil: Table | None = None
    table_miscellaneous: Table | None = None
