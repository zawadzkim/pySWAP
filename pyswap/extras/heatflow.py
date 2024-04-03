"""Heat flow"""
from pyswap.core.utils.basemodel import PySWAPBaseModel
from pyswap.core.utils.fields import Table
from typing import Literal, Optional


class HeatFlow(PySWAPBaseModel):

    swhea: Literal[0, 1]
    swcalt: Optional[Literal[0, 1]] = None
    tampli: Optional[float] = None
    tmean: Optional[float] = None
    timref: Optional[float] = None
    ddamp: Optional[float] = None
    swtopbhea: Optional[Literal[0, 1]] = None
    tsoilfile: Optional[str] = None
    swbotbhea: Optional[Literal[0, 1]] = None
    table_soiltextures: Optional[Table] = None
    table_initsoil: Optional[Table] = None
    table_bbctsoil: Optional[Table] = None
