# mypy: disable-error-code="call-overload, misc"

"""Lateral drainage settings

Settings for the lateral drainage of the .swp file, including the .dra file settings.

Classes:
    Flux: Fluxes between drainage levels in .dra file.
    DraFile: Drainage file (.dra) settings.
    Drainage: The lateral drainage settings of .swp file.
"""

from typing import Literal as _Literal

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import (
    DATOWLTB1,
    DATOWLTB2,
    DATOWLTB3,
    DATOWLTB4,
    DATOWLTB5,
    DRAINAGELEVELTOPPARAMS,
    DRNTB,
    MANSECWATLVL,
    PRIWATLVL,
    QDRNTB,
    QWEIR,
    QWEIRTB,
    SECWATLVL,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import FNAME_IN as _FNAME_IN
from pyswap.core.fields import (
    File as _File,
    FloatList as _FloatList,
    String as _String,
    Subsection as _Subsection,
    Table as _Table,
)
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "DATOWLTB1",
    "DATOWLTB2",
    "DATOWLTB3",
    "DATOWLTB4",
    "DATOWLTB5",
    "DRAINAGELEVELTOPPARAMS",
    "DRNTB",
    "MANSECWATLVL",
    "PRIWATLVL",
    "QDRNTB",
    "QWEIR",
    "QWEIRTB",
    "SECWATLVL",
    "DraFile",
    "Drainage",
    "Flux",
]


class Flux(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Fluxes between drainage levels in .dra file.

    !!! note

        This was rewritten to be a single class instead of a list of classes.
        Simplicity over DRY. Anyway, the prefered way to set this up would be
        through the table from the extended section I guess.

    Attributes:
        drares (float): Drainage resistance [10 .. 1e5 d].
        infres (float): Infiltration resistance [10 .. 1e5 d].
        swallo (Literal[1, 2]): Switch to allow drainage from this level.

            * 1 - Drainage and infiltration are both allowed.
            * 2 - Only infiltration is allowed.
            * 3 - Only drainage is allowed.

        l (Optional[float]): Drain spacing [1 .. 1e5 m].
        zbotdr (float): Level of the bottom of the drain [-1e4 .. 0 cm].
        swdtyp (Literal[1, 2]): Drainage type.

            * 1 - drain tube.
            * 2 - open channel.

        datowltb (Table): date DATOWL [date] and channel water
            level LEVEL. Add suffix to the dataframe headers
            according to the level number.
    """

    drares1: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres1: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo1: _Literal[1, 2, 3] | None = None
    l1: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr1: float = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp1: _Literal[1, 2] | None = None
    datowltb1: _Table | None = None
    # level 2
    drares2: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres2: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo2: _Literal[1, 2, 3] | None = None
    l2: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr2: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp2: _Literal[1, 2] | None = None
    datowltb2: _Table | None = None
    # level 3
    drares3: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres3: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo3: _Literal[1, 2, 3] | None = None
    l3: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr3: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp3: _Literal[1, 2] | None = None
    datowltb3: _Table | None = None
    # level 4
    drares4: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres4: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo4: _Literal[1, 2, 3] | None = None
    l4: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr4: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp4: _Literal[1, 2] | None = None
    datowltb4: _Table | None = None
    # level 5
    drares5: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    infres5: float | None = _Field(default=None, ge=10.0, le=1.0e5)
    swallo5: _Literal[1, 2, 3] | None = None
    l5: float | None = _Field(default=None, ge=1.0, le=1.0e5)
    zbotdr5: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    swdtyp5: _Literal[1, 2] | None = None
    datowltb5: _Table | None = None


class DraFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Content of the drainage file (.dra).

    Attributes general:
        dramet (Literal[1, 2, 3]): Method of lateral drainage calculation

            * 1 - Use table of drainage flux - groundwater level relation.
            * 2 - Use drainage formula of Hooghoudt or Ernst.
            * 3 - Use drainage/infiltration resistance, multi-level if needed.

        swdivd (Literal[1, 2]): Calculate vertical distribution of
            drainage flux in groundwater.
        cofani (Optional[FloatList]): specify anisotropy factor COFANI
            (horizontal/vertical saturated hydraulic conductivity) for
            each soil layer (maximum MAHO)
        swdislay (Literal[0, 1, 2, 3, '-']): Switch to adjust
            upper boundary of model discharge layer.

            * 0 - No adjustment
            * 1 - Adjustment based on depth of top of model discharge
            * 2 - Adjustment based on factor of top of model discharge

    Attributes drainage flux table (option 1):
        lm1 (float): Drain spacing
        table_qdrntb (Table): Table of drainage flux - groundwater level.

    Attributes drainage formula (option 2):
        lm2 (float): Drain spacing.
        shape (float): Shape factor to account for actual location between
            drain and water divide.
        wetper (float): Wet perimeter of the drain.
        zbotdr (float): Level of drain bottom.
        entres (float): Drain entry resistance.
        ipos (Literal[1, 2, 3, 4, 5]): Position of drain

            * 1 - On top of an impervious layer in a homogeneous profile
            * 2 - Above an impervious layer in a homogeneous profile
            * 3 - At the interface of a fine upper and a coarse lower
                soil layer
            * 4 - In the lower, more coarse soil layer
            * 5 - In the upper, more fine soil layer

        basegw (float): Level of impervious layer.
        khtop (float): Horizontal hydraulic conductivity of the top layer.
        khbot (Optional[float]): Horizontal hydraulic conductivity of
            the bottom layer.
        zintf (Optional[float]): Interface level of the coarse and
            fine soil layer.
        kvtop (Optional[float]): Vertical hydraulic conductivity of
            the top layer.
        kvbot (Optional[float]): Vertical hydraulic conductivity of
            the bottom layer.
        geofac (Optional[float]): Geometric factor of Ernst.

    Attributes drainage infiltration resistance (option 3):
        nrlevs (int): Number of drainage levels.
        swintfl (Literal[0, 1]): Option for interflow in highest
            drainage level (shallow system with short residence time).
        cofintflb (float): Coefficient for interflow relation.
        expintflb (float): Exponent for interflow relation.
        swtopnrsrf (Literal[0, 1]): Switch to enable adjustment of
            model discharge layer.
        fluxes (Flux): Flux object containing parameters for each drainage level.

    Attributes extended section (surface water management):
        altcu (float): Altitude of the control unit relative to reference level.
        nrsrf (int): Number of subsurface drainage levels.
        swnrsrf (Literal[0, 1, 2]): Switch to introduce rapid subsurface drainage.
        rsurfdeep (Optional[float]): Maximum resistance of rapid subsurface drainage.
        rsurfshallow (Optional[float]): Minimum resistance of rapid subsurface drainage.
        swsrf (Literal[1, 2, 3]): Switch for interaction with surface water system.
        swsec (Optional[Literal[1, 2]]): Option for surface water level of secondary system.
        wlact (Optional[float]): Initial surface water level.
        osswlm (Optional[float]): Criterium for warning about oscillation.
        nmper (Optional[int]): Number of management periods.
        swqhr (Optional[Literal[1, 2]]): Switch for type of discharge relationship.
        sofcu (Optional[float]): Size of the control unit.
    """

    _extension = _PrivateAttr("dra")
    # General
    dramet: _Literal[1, 2, 3] | None = None
    swdivd: _Literal[1, 2] | None = None
    cofani: _FloatList | None = None
    swdislay: _Literal[0, 1, 2, 3, "-"] | None = None
    # Drainage flux table
    lm1: float | None = _Field(default=None, ge=1.0, le=1000.0)
    qdrntb: _Table | None = None
    # Drainage formula
    lm2: float | None = _Field(default=None, ge=1.0, le=1000.0)
    shape: float | None = _Field(default=None, **_UNITRANGE)
    wetper: float | None = _Field(default=None, ge=0.0, le=1000.0)
    zbotdr: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    entres: float | None = _Field(default=None, ge=0.0, le=1000.0)
    ipos: _Literal[1, 2, 3, 4, 5] | None = None
    basegw: float | None = _Field(default=None, ge=-1.0e4, le=0.0)
    khtop: float | None = _Field(default=None, ge=0.0, le=1000.0)
    khbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    zintf: float | None = _Field(default=None, ge=-1.0e4, le=0.0)
    kvtop: float | None = _Field(default=None, ge=0.0, le=1000.0)
    kvbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    geofac: float | None = _Field(default=None, ge=0.0, le=100.0)
    # Drainage infiltration resistance
    nrlevs: int | None = _Field(default=None, ge=1, le=5)
    swintfl: _Literal[0, 1] | None = None
    cofintflb: float | None = _Field(default=None, ge=0.01, le=10.0)
    expintflb: float | None = _Field(default=None, ge=0.1, le=1.0)
    swtopnrsrf: _Literal[0, 1] | None = None
    fluxes: _Subsection | None = None
    # Extended section
    altcu: float | None = _Field(default=None, ge=-300000.0, le=300000.0)
    drntb: _Table | None = None
    nrsrf: int | None = _Field(default=None, ge=1, le=5)
    swnrsrf: _Literal[0, 1, 2] | None = None
    rsurfdeep: float | None = _Field(default=None, ge=0.001, le=1000.0)
    rsurfshallow: float | None = _Field(default=None, ge=0.001, le=1000.0)
    cofintfl: float | None = _Field(default=None, ge=0.01, le=10.0)
    expintfl: float | None = _Field(default=None, ge=0.01, le=10.0)
    swsrf: _Literal[1, 2, 3] | None = None
    swsec: _Literal[1, 2] | None = None
    secwatlvl: _Table | None = None
    wlact: float | None = _Field(default=None, ge=-300000.0, le=300000.0)
    osswlm: float | None = _Field(default=None, ge=0.0, le=10.0)
    nmper: int | None = _Field(default=None, ge=1, le=3660)
    swqhr: _Literal[1, 2] | None = None
    sofcu: float | None = _Field(default=None, ge=0.1, le=100000.0)
    mansecwatlvl: _Table | None = None
    drainageleveltopparams: _Table | None = None
    qweir: _Table | None = None
    qweirtb: _Table | None = None
    priwatlvl: _Table | None = None

    @property
    def dra(self):
        return self.model_string()


class Drainage(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """The lateral drainage settings inside .swp file.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0 - No drainage.
            * 1 - Simulate with a basic drainage routine.
            * 2 - Simulate with surface water management.

        drfil (str): Name of the file. This attribute is frozen, there is no
            need to change it.
        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: _Literal[0, 1, 2] | None = None
    drfil: _String | None = _Field(default=_FNAME_IN, frozen=True)
    drafile: _File | None = _Field(default=None, exclude=True)

    def write_dra(self, path: str) -> None:
        self.drafile.save_file(string=self.drafile.dra, fname=self.drfil, path=path)
        return None
