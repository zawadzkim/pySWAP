import pandera as pa
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String, Table
from pyswap.core.mixins import SerializableMixin, YAMLValidatorMixin


from typing import Literal

from pyswap.core.basemodel import BaseTableModel

__all__ = ["HeatFlow", "SoluteTransport", "SOILTEXTURES", "INITSOILTEMP"]


class HeatFlow(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Heat flow settings for SWAP simulation.

    Attributes:
        swhea (Literal[0, 1]): Switch for heat flow.
        swcalt (Optional[Literal[1, 2]]):
            * 1 - analytical method
            * 2 - numerical method
        tampli (Optional[Decimal2f]): Amplitude of annual temperature wave at soil surface [0..50 oC, R]
        tmean (Optional[Decimal2f]): Mean annual temperature at soil surface [-10..30 oC, R]
        timref (Optional[Decimal2f]): Time at which the sinus temperature wave reaches its top [0..366.0 d, R]
        ddamp (Optional[Decimal2f]): Damping depth of soil temperature wave [1..500 cm, R]
        swtopbhea (Optional[Literal[1, 2]]): Define top boundary condition
            * 1 - use air temperature of meteo input file as top boundary
            * 2 - use measured top soil temperature as top boundary
        tsoilfile (Optional[str]): Name of input file with soil surface temperatures without extension .TSS
        swbotbhea (Optional[Literal[1, 2]]): Define bottom boundary condition
            * 1 - no heat flux
            * 2 - prescribe bottom temperature
        soiltextures (Optional[Table]): For each physical soil layer the soil texture (g/g mineral parts) and the organic matter content (g/g dry soil)
        initsoil (Optional[Table]): Initial temperature TSOIL [-50..50 oC, R] as function of soil depth ZH [-100000..0 cm, R]
        bbctsoil (Optional[Table]): Bottom boundary temperature TBOT [-50..50 oC, R] as function of date DATET [date]
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
    """Solute transport settings.

    Attributes:

        swsolu (Literal[0, 1]): Switch for simulation of solute transport.
        cpre (Optional[Decimal2f]): Solute concentration in precipitation [0..100 mg/cm3].
        cdrain (Optional[Decimal2f]): Solute concentration in surface water [0..100 mg/cm3].
        swbotbc (Optional[Literal[0, 1, 2]]): Switch for groundwater concentration in case of upward flow (seepage).
        cseep (Optional[Decimal2f]): Solute concentration in surface water [0..100 mg/cm3].
        ddif (Optional[Decimal2f]): Molecular diffusion coefficient [0..10 cm2/d].
        tscf (Optional[Decimal2f]): Relative uptake of solutes by roots [0..10].
        swsp (Optional[Literal[0, 1]]): Switch, consider solute adsorption.
        frexp (Optional[Decimal2f]): Freundlich exponent [0..10].
        cref (Optional[Decimal2f]): Reference solute concentration for adsorption [0..1000 mg/cm3].
        swdc (Optional[Literal[0, 1]]): Switch, consider solute decomposition.
        gampar (Optional[Decimal2f]): Factor reduction decomposition due to temperature [0..0.5 /C].
        rtheta (Optional[Decimal2f]): Minimum water content for potential decomposition [0..0.4 cm3/cm3].
        bexp (Optional[Decimal2f]): Exponent in reduction decomposition due to dryness [0..2].
        swbr (Optional[Literal[0, 1]]): Switch, consider mixed reservoir of saturated zone.
        daquif (Optional[Decimal2f]): Thickness saturated part of aquifer [0..10000 cm].
        poros (Optional[Decimal2f]): Porosity of aquifer [0..0.6].
        kfsat (Optional[Decimal2f]): Linear adsorption coefficient in aquifer [0..100 cm3/mg].
        decsat (Optional[Decimal2f]): Decomposition rate in aquifer [0..10 /d].
        cdraini (Optional[Decimal2f]): Initial solute concentration in groundwater [0..100 mg/cm3].
        cseeparrtb (Optional[Table]): Table for groundwater concentration as function of time.
        inissoil (Optional[Table]): Table for initial solute concentration as function of soil depth.
        miscellaneous (Optional[Table]): Table for miscellaneous parameters as function of soil depth.
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