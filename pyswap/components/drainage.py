"""
## Lateral drainage settings

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


from typing import Literal

from pydantic import Field

from pyswap.core.fields import FloatList, ObjectList, String, Table, File, Subsection
from pyswap.core.valueranges import UNITRANGE
from pyswap.core.mixins import YAMLValidatorMixin, FileMixin, SerializableMixin
from pyswap.core.basemodel import PySWAPBaseModel

__all__ = [
    "DraSettings",
    "DrainageFluxTable",
    "DrainageFormula",
    "DrainageInfRes",
    "Flux",
    "DraFile",
    "Drainage",
]


class DraSettings(PySWAPBaseModel, SerializableMixin):
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

    dramet: Literal[1, 2, 3]
    swdivd: Literal[1, 2]
    cofani: FloatList | None
    swdislay: Literal[0, 1, 2, 3, "-"]


class DrainageFluxTable(PySWAPBaseModel, SerializableMixin):
    """Settings for the case when dramet is 1 in .dra file.

    Attributes:
        lm1 (float): Drain spacing
        table_qdrntb (Table): Table of drainage flux - groundwater level.
    """

    lm1: float = Field(ge=1.0, le=1000.0)
    qdrntb: Table


class DrainageFormula(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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

    lm2: float = Field(ge=1.0, le=1000.0)
    shape: float = Field(**UNITRANGE)
    wetper: float = Field(ge=0.0, le=1000.0)
    zbotdr: float = Field(ge=-1000.0, le=0.0)
    entres: float = Field(ge=0.0, le=1000.0)
    ipos: Literal[1, 2, 3, 4, 5]
    basegw: float = Field(ge=-1.0e4, le=0.0)
    khtop: float = Field(ge=0.0, le=1000.0)
    khbot: float | None = Field(default=None, ge=0.0, le=1000.0)
    zintf: float | None = Field(default=None, ge=-1.0e4, le=0.0)
    kvtop: float | None = Field(default=None, ge=0.0, le=1000.0)
    kvbot: float | None = Field(default=None, ge=0.0, le=1000.0)
    geofac: float | None = Field(default=None, ge=0.0, le=100.0)


class DrainageInfRes(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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

    nrlevs: int = Field(ge=1, le=5)
    swintfl: Literal[0, 1]
    cofintflb: float | None = Field(default=None, ge=0.01, le=10.0)
    expintflb: float | None = Field(default=None, ge=0.1, le=1.0)
    swtopnrsrf: Literal[0, 1] | None = None
    levelfluxes: ObjectList | None = None


class Flux(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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

    level_number: int = Field(exclude=True, ge=1, le=5)
    drares: float = Field(ge=10.0, le=1.0e5)
    infres: float = Field(ge=10.0, le=1.0e5)
    swallo: Literal[1, 2, 3]
    l: float | None = Field(ge=1.0, le=1.0e5)
    zbotdr: float = Field(ge=-1000.0, le=0.0)
    swdtyp: Literal[1, 2]
    table_datowltb: Table

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


class DraFile(PySWAPBaseModel, FileMixin, SerializableMixin):
    """Drainage file (.dra) settings.

    Attributes:
        drfil (str): Name of the file.
        general (Any): General settings.
        fluxtable (Optional[Any]): Flux table.
        drainageformula (Optional[Any]): Drainage formula.
        drainageinfres (Optional[Any]): Drainage infiltration resistance.
    """

    drfil: String
    general: Subsection | None = None
    fluxtable: Subsection | None = None
    drainageformula: Subsection | None = None
    drainageinfres: Subsection | None = None


class Drainage(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """The lateral drainage settings of .swp file.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0 - No drainage.
            * 1 - Simulate with a basic drainage routine.
            * 2 - Simulate with surface water management.

        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: Literal[0, 1, 2]
    drafile: File | None = Field(default=None)

    @property
    def dra(self):
        return self.model_string()

    def write_dra(self, path: str):
        self.drafile.save_file(
            string=self.dra, extension="dra", fname=self.drafile.drfil, path=path
        )

        print("dra file saved.")

