"""Lateral drainage settings

Settings for the lateral drainage of the .swp file, including the .dra file settings.

Classes:
    DraSettings: General section of the .dra file.
    DrainageFluxTable: Settings for the case when dramet is 1 in .dra file.
    DrainageFormula: Settings for the case when dramet is 2 in .dra file.
    DrainageInfRes: Settings for the case when dramet is 3 in .dra file.
    Flux: Fluxes between drainage levels in .dra file.
    DraFile: Drainage file (.dra) settings.
    Drainage: The lateral drainage settings of .swp file.
"""

from typing import Literal as _Literal

from pydantic import Field as _Field, PrivateAttr as _PrivateAttr

from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import File as _File, FloatList as _FloatList, ObjectList as _ObjectList, String as _String, Subsection as _Subsection, Table as _Table
from pyswap.core.mixins import FileMixin as _FileMixin, SerializableMixin as _SerializableMixin, YAMLValidatorMixin as _YAMLValidatorMixin
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE

__all__ = [
    "DraSettings",
    "DrainageFluxTable",
    "DrainageFormula",
    "DrainageInfRes",
    "Flux",
    "DraFile",
    "Drainage",
]


class DraSettings(_PySWAPBaseModel, _SerializableMixin):
    """General section of the .dra file.

    Attributes:
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
            * 1 - Adjusment based on depth of top of model discharge
            * 2 - Adjusment based on factor of top of model discharge
    """

    dramet: _Literal[1, 2, 3]
    swdivd: _Literal[1, 2]
    cofani: _FloatList | None
    swdislay: _Literal[0, 1, 2, 3, "-"]


class DrainageFluxTable(_PySWAPBaseModel, _SerializableMixin):
    """Settings for the case when dramet is 1 in .dra file.

    Attributes:
        lm1 (float): Drain spacing
        table_qdrntb (Table): Table of drainage flux - groundwater level.
    """

    lm1: float = _Field(ge=1.0, le=1000.0)
    qdrntb: _Table


class DrainageFormula(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings for the case when dramet is 2 in .dra file.

    Attributes:
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
    """

    lm2: float = _Field(ge=1.0, le=1000.0)
    shape: float = _Field(**_UNITRANGE)
    wetper: float = _Field(ge=0.0, le=1000.0)
    zbotdr: float = _Field(ge=-1000.0, le=0.0)
    entres: float = _Field(ge=0.0, le=1000.0)
    ipos: _Literal[1, 2, 3, 4, 5]
    basegw: float = _Field(ge=-1.0e4, le=0.0)
    khtop: float = _Field(ge=0.0, le=1000.0)
    khbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    zintf: float | None = _Field(default=None, ge=-1.0e4, le=0.0)
    kvtop: float | None = _Field(default=None, ge=0.0, le=1000.0)
    kvbot: float | None = _Field(default=None, ge=0.0, le=1000.0)
    geofac: float | None = _Field(default=None, ge=0.0, le=100.0)


class DrainageInfRes(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings for the case when dramet is 3 in .dra file.

    Attributes:
        nrlevs (int): Number of drainage levels.
        swintfl (Literal[0, 1]): Option for interflow in highest
            drainage level (shallow system with short residence time).
        cofintflb (float): Coefficient for interflow relation.
        expintflb (float): Exponent for interflow relation.
        swtopnrsrf (Literal[0, 1]): Switch to enable adjustment of
            model discharge layer.
        list_levelfluxes (ObjectList): List of level fluxes.
    """

    nrlevs: int = _Field(ge=1, le=5)
    swintfl: _Literal[0, 1]
    cofintflb: float | None = _Field(default=None, ge=0.01, le=10.0)
    expintflb: float | None = _Field(default=None, ge=0.1, le=1.0)
    swtopnrsrf: _Literal[0, 1] | None = None
    levelfluxes: _ObjectList | None = None


class Flux(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Fluxes between drainage levels in .dra file.

    !!! note

        These objects are needed for the DrainageInfiltrationResitance class.
        Flux object should be created for each level of drainage.

    Attributes:
        level_number (int): Number of the level.
        drares (float): Drainage resistance.
        infres (float): Infiltration resistance.
        swallo (Literal[1, 2]): Switch to allow drainage from this level.
        l (Optional[float]): Drain spacing.
        zbotdr (float): Level of the bottom of the drain.
        swdtyp (Literal[1, 2]): Drainage type.

            * 1 - drain tube.
            * 2 - open channel.

        table_datowltb (Table): date DATOWL [date] and channel water
            level LEVEL. Add suffix to the dataframe headers
            according to the level number.
    """

    level_number: int = _Field(exclude=True, ge=1, le=5)
    drares: float = _Field(ge=10.0, le=1.0e5)
    infres: float = _Field(ge=10.0, le=1.0e5)
    swallo: _Literal[1, 2, 3]
    l: float | None = _Field(ge=1.0, le=1.0e5)
    zbotdr: float = _Field(ge=-1000.0, le=0.0)
    swdtyp: _Literal[1, 2]
    table_datowltb: _Table

    def model_dump(self, **kwargs):
        d = super().model_dump(**kwargs)

        # If level_number is set, modify the key names.
        if self.level_number is not None:
            new_d = {}
            suffix = str(self.level_number)
            for key, value in d.items():
                new_d[key + suffix] = value
            return new_d
        return d


class DraFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Drainage file (.dra) settings.

    Attributes:
        drfil (str): Name of the file.
        general (Any): General settings.
        fluxtable (Optional[Any]): Flux table.
        drainageformula (Optional[Any]): Drainage formula.
        drainageinfres (Optional[Any]): Drainage infiltration resistance.
    """

    _extension = _PrivateAttr("dra")

    drfil: _String
    general: _Subsection | None = None
    fluxtable: _Subsection | None = None
    drainageformula: _Subsection | None = None
    drainageinfres: _Subsection | None = None


class Drainage(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """The lateral drainage settings inside .swp file.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0 - No drainage.
            * 1 - Simulate with a basic drainage routine.
            * 2 - Simulate with surface water management.

        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: _Literal[0, 1, 2] | None = None
    drafile: _File | None = _Field(default=None)

    @property
    def dra(self):
        return self.model_string()

    def write_dra(self, path: str) -> None:
        self.drafile.save_file(string=self.dra, fname=self.drafile.drfil, path=path)
        return None
