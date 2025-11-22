# mypy: disable-error-code="call-overload, misc, override"

from typing import Literal as _Literal

from pydantic import Field as _Field

from pyswap.components.tables import INITSOILTEMP, SOILTEXTURES
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Decimal2f as _Decimal2f,
    String as _String,
    Table as _Table,
)
from pyswap.core.valueranges import YEARRANGE as _YEARRANGE
from pyswap.utils.mixins import (
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = ["INITSOILTEMP", "SOILTEXTURES", "HeatFlow", "SoluteTransport"]


class HeatFlow(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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
        initsoiltemp (Optional[Table]): Initial temperature TSOIL [-50..50 oC, R] as function of soil depth ZH [-100000..0 cm, R]
        bbctsoil (Optional[Table]): Bottom boundary temperature TBOT [-50..50 oC, R] as function of date DATET [date]
    """

    swhea: _Literal[0, 1] | None = None
    swcalt: _Literal[1, 2] | None = None
    tampli: _Decimal2f | None = _Field(None, ge=0, le=50)
    tmean: _Decimal2f | None = _Field(None, ge=-10, le=30)
    timref: _Decimal2f | None = _Field(None, **_YEARRANGE)
    ddamp: _Decimal2f | None = _Field(None, ge=1, le=500)
    swtopbhea: _Literal[1, 2] | None = None
    tsoilfile: _String | None = None
    swbotbhea: _Literal[1, 2] | None = None
    soiltextures: _Table | None = None
    initsoiltemp: _Table | None = None
    bbctsoil: _Table | None = None


class SoluteTransport(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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

    swsolu: _Literal[0, 1] | None = None
    cpre: _Decimal2f | None = _Field(None, ge=0, le=100)
    cdrain: _Decimal2f | None = _Field(None, ge=0, le=100)
    swbotbc: _Literal[0, 1, 2] | None = None
    cseep: _Decimal2f | None = _Field(None, ge=0, le=100)
    ddif: _Decimal2f | None = _Field(None, ge=0, le=10)
    tscf: _Decimal2f | None = _Field(None, ge=0, le=10)
    swsp: _Literal[0, 1] | None = None
    frexp: _Decimal2f | None = _Field(None, ge=0, le=10)
    cref: _Decimal2f | None = _Field(None, ge=0, le=1000)
    swdc: _Literal[0, 1] | None = None
    gampar: _Decimal2f | None = _Field(None, ge=0, le=0.5)
    rtheta: _Decimal2f | None = _Field(None, ge=0, le=0.4)
    bexp: _Decimal2f | None = _Field(None, ge=0, le=2)
    swbr: _Literal[0, 1] | None = None
    daquif: _Decimal2f | None = _Field(None, ge=0, le=10000)
    poros: _Decimal2f | None = _Field(None, ge=0, le=0.6)
    kfsat: _Decimal2f | None = _Field(None, ge=0, le=100)
    decsat: _Decimal2f | None = _Field(None, ge=0, le=10)
    cdraini: _Decimal2f | None = _Field(None, ge=0, le=100)
    cseeparrtb: _Table | None = None
    inissoil: _Table | None = None
    misc: _Table | None = None
