import pandera as pa
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String, Table, Decimal2f
from pyswap.core.valueranges import YEARRANGE
from pyswap.core.mixins import SerializableMixin, YAMLValidatorMixin
from pyswap.components.tables import SOILTEXTURES, INITSOILTEMP

from typing import Literal
from pydantic import Field

__all__ = ["HeatFlow", "SoluteTransport"]


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

    swhea: Literal[0, 1] | None = None
    swcalt: Literal[1, 2] | None = None
    tampli: Decimal2f | None = Field(None, ge=0, le=50)
    tmean: Decimal2f | None = Field(None, ge=-10, le=30)
    timref: Decimal2f | None = Field(None, **YEARRANGE)
    ddamp: Decimal2f | None = Field(None, ge=1, le=500)
    swtopbhea: Literal[1, 2] | None = None
    tsoilfile: String | None = None
    swbotbhea: Literal[1, 2] | None = None
    soiltextures: Table | None = None
    initsoil: Table | None = None
    bbctsoil: Table | None = None


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

    swsolu: Literal[0, 1] | None = None
    cpre: Decimal2f | None = Field(None, ge=0, le=100)
    cdrain: Decimal2f | None = Field(None, ge=0, le=100)
    swbotbc: Literal[0, 1, 2] | None = None
    cseep: Decimal2f | None = Field(None, ge=0, le=100)
    ddif: Decimal2f | None = Field(None, ge=0, le=10)
    tscf: Decimal2f | None = Field(None, ge=0, le=10)
    swsp: Literal[0, 1] | None = None
    frexp: Decimal2f | None = Field(None, ge=0, le=10)
    cref: Decimal2f | None = Field(None, ge=0, le=1000)
    swdc: Literal[0, 1] | None = None
    gampar: Decimal2f | None = Field(None, ge=0, le=0.5)
    rtheta: Decimal2f | None = Field(None, ge=0, le=0.4)
    bexp: Decimal2f | None = Field(None, ge=0, le=2)
    swbr: Literal[0, 1] | None = None
    daquif: Decimal2f | None = Field(None, ge=0, le=10000)
    poros: Decimal2f | None = Field(None, ge=0, le=0.6)
    kfsat: Decimal2f | None = Field(None, ge=0, le=100)
    decsat: Decimal2f | None = Field(None, ge=0, le=10)
    cdraini: Decimal2f | None = Field(None, ge=0, le=100)
    cseeparrtb: Table | None = None
    inissoil: Table | None = None
    misc: Table | None = None


transport_tables = ["SOILTEXTURES", "INITSOILTEMP"]
__all__.extend(transport_tables)
