import pandera as pa
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String, Table
from pyswap.core.mixins import SerializableMixin, YAMLValidatorMixin


from typing import Literal

from pyswap.core.basemodel import BaseTableModel

__all__ = ["HeatFlow", "SoluteTransport", "SOILTEXTURES", "INITSOILTEMP"]


class HeatFlow(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Heat flow settings for SWAP simulation.

    !!! warning

        table_initsoil is not validated because it depends of swinco setting.

    Attributes:
        swhea (Literal[0, 1]): Switch for heat flow.
        swcalt (Optional[Literal[1, 2]]):

            * 1 - analytical method
            * 2 - numerical method

        tampli (Optional[float]): Amplitude of annual temperature wave atsoil
            surface [0..50 oC, R]
        tmean (Optional[float]): Mean annual temperature at
            soil surface[-10..30 oC, R]
        timref (Optional[float]): Time at which the sinus temperature
            wave reaches it's top [0..366.0 d, R]
        ddamp (Optional[float]): Damping depth of soil temperature
            wave[1..500 cm, R]
        swtopbhea (Optional[Literal[1, 2]]): Define top boundary condition

            * 1 - use air temperature of meteo input file as top boundary
            * 2 - use measured top soil temperature as top boundary

        tsoilfile (Optional[str]): name of input file with soil
            surface temperatures without extension .TSS
        swbotbhea (Optional[Literal[1, 2]]): Define bottom boundary condition

            * 1 - no heat flux
            * 2 - prescribe bottom temperature

        table_soiltextures (Optional[Table]): for each physical
            soil layer the soil texture (g/g mineral parts) and the
            organic matter content (g/g dry soil)
        table_initsoil (Optional[Table]): initial temperature TSOIL
            [-50..50 oC, R] as function of soil depth ZH [-100000..0 cm, R]
        table_bbctsoil (Optional[Table]): bottom boundary temperature TBOT
            [-50..50 oC, R] as function of date DATET [date]
    """

    swhea: Literal[0, 1]
    swcalt: Literal[1, 2] | None = None
    tampli: float | None = None
    tmean: float | None = None
    timref: float | None = None
    ddamp: float | None = None
    swtopbhea: Literal[1, 2] | None = None
    tsoilfile: String | None = None
    swbotbhea: Literal[1, 2] | None = None
    table_soiltextures: Table | None = None
    table_initsoil: Table | None = None
    table_bbctsoil: Table | None = None


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