"""These are tables for the extras module"""

import pandera as pa

from ..core.tablevalidation import BaseTableModel


class SOILTEXTURES(BaseTableModel):
    """Table for soil textures.

    Attributes:
        PSAND (float): Depth of soil layer [cm, R]
        PSILT (float): Sand content [g/g mineral parts, R]
        PCLAY (float): Clay content [g/g mineral parts, R]
        ORGMAT (float): Organic matter content [g/g dry soil, R]
    """

    PSAND: float
    PSILT: float
    PCLAY: float
    ORGMAT: float


class INITSOILTEMP(BaseTableModel):
    """Table for initial soil temperature.

    Attributes:
        ZH (float): Depth of soil layer [cm, R]
        TSOIL (float): Initial temperature [oC, R]
    """

    ZH: float = pa.Field(ge=-100000, le=0)
    TSOIL: float = pa.Field(ge=-50, le=50)
