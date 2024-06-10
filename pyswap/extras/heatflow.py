"""Heat flow settings for SWAP simulation.

Classes:
    HeatFlow: Heat flow settings for SWAP simulation.
"""
from pyswap.core.utils.basemodel import PySWAPBaseModel
from pyswap.core.utils.fields import Table
from typing import Literal, Optional


class HeatFlow(PySWAPBaseModel):
    """Heat flow settings for SWAP simulation.

    Attributes:
        swhea (Literal[0, 1]): Switch for heat flow.
        swcalt (Optional[Literal[1, 2]]):

            * 1 - analytical method
            * 2 - numerical method

        tampli (Optional[float]):
        tmean (Optional[float]):
        timref (Optional[float]):
        ddamp (Optional[float]):
        swtopbhea (Optional[Literal[0, 1]]):
        tsoilfile (Optional[str]):
        swbotbhea (Optional[Literal[0, 1]]):
        table_soiltextures (Optional[Table]):
        table_initsoil (Optional[Table]):
        table_bbctsoil (Optional[Table]):
    """

    swhea: Literal[0, 1]
    swcalt: Optional[Literal[1, 2]] = None
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
