"""
Compose the .dra file for SWAP simulation.

Classes:
    DraFile: Class for the .dra file.
    DraSettings: Class for the settings of the drainage module.
    DrainageFluxTable: Class for the drainage flux table.
    DrainageFormula: Class for the drainage formula.
    DrainageInfiltrationResitance: Class for the drainage infiltration resistance.
    Flux: Class for the flux.
"""
from ..core import (PySWAPBaseModel, FloatList, Table,
                    ObjectList, UNITRANGE)
from pydantic import Field, model_validator
from typing import Literal, Optional
from typing_extensions import Self


class DraSettings(PySWAPBaseModel):
    """General settings for the drainage file

    Attributes:
        dramet (Literal[1, 2, 3]): Method of lateral drainage calculation

            * 1 - Use table of drainage flux - groundwater level relation.
            * 2 - Use drainage formula of Hooghoudt or Ernst.
            * 3 - Use drainage/infiltration resistance, multi-level if needed.

        swdivd (Literal[1, 2]): Calculate vertical distribution of drainage flux in groundwater.
        cofani (Optional[FloatList]): specify anisotropy factor COFANI (horizontal/vertical saturated hydraulic conductivity) for each soil layer (maximum MAHO)
        swdislay (Literal[0, 1, 2, 3, '-']): Switch to adjust upper boundary of model discharge layer.

            * 0 - No adjustment
            * 1 - Adjusment based on depth of top of model discharge
            * 2 - Adjusment based on factor of top of model discharge

    """
    dramet: Literal[1, 2, 3]
    swdivd: Literal[1, 2]
    cofani: Optional[FloatList]
    swdislay: Literal[0, 1, 2, 3, '-']


class DrainageFluxTable(PySWAPBaseModel):
    """Settings for the case when dramet is 1.

    Attributes:
        lm1 (float): Drain spacing
        table_qdrntb (Table): Table of drainage flux - groundwater level.
    """
    lm1: float = Field(ge=1.0, le=1000.0)
    table_qdrntb: Table


class DrainageFormula(PySWAPBaseModel):
    """Settings for the case when dramet is 2.

    Attributes:
        lm2 (float): Drain spacing.
        shape (float): Shape factor to account for actual location between drain and water divide.
        wetper (float): Wet perimeter of the drain.
        zbotdr (float): Level of drain bottom.
        entres (float): Drain entry resistance.
        ipos (Literal[1, 2, 3, 4, 5]): Position of drain

            * 1 - On top of an impervious layer in a homogeneous profile
            * 2 - Above an impervious layer in a homogeneous profile
            * 3 - At the interface of a fine upper and a coarse lower soil layer
            * 4 - In the lower, more coarse soil layer
            * 5 - In the upper, more fine soil layer
        basegw (float): Level of impervious layer.
        khtop (float): Horizontal hydraulic conductivity of the top layer.
        khbot (Optional[float]): Horizontal hydraulic conductivity of the bottom layer.
        zintf (Optional[float]): Interface level of the coarse and fine soil layer.
        kvtop (Optional[float]): Vertical hydraulic conductivity of the top layer.
        kvbot (Optional[float]): Vertical hydraulic conductivity of the bottom layer.
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
    khbot: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    zintf: Optional[float] = Field(default=None, ge=-1.0e4, le=0.0)
    kvtop: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    kvbot: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    geofac: Optional[float] = Field(default=None, ge=0.0, le=100.0)

    @model_validator(mode='after')
    def _validate_draformula(self) -> Self:
        if self.ipos in [3, 4, 5]:
            assert self.khbot is not None, 'khbot has to be provided if IPOS is 3.'
            assert self.zintf is not None, 'zintf has to be provided if IPOS is 3.'
        if self.ipos in [4, 5]:
            assert self.kvtop is not None, 'kvtop has to be provided if IPOS is 3.'
            assert self.kvbot is not None, 'kvbot has to be provided if IPOS is 3.'
        if self.ipos == 5:
            assert self.geofac is not None, 'geofac has to be provided if IPOS is 3.'

        return self


class DrainageInfiltrationResitance(PySWAPBaseModel):
    """Settings for the case when dramet is 3.

    Attributes:
        nrlevs (int): Number of drainage levels.
        swintfl (Literal[0, 1]): Option for interflow in highest drainage level (shallow system with short residence time).
        cofintflb (float): Coefficient for interflow relation.
        expintflb (float): Exponent for interflow relation.
        swtopnrsrf (Literal[0, 1]): Switch to enable adjustment of model discharge layer.
        list_levelfluxes (ObjectList): List of level fluxes.
    """
    nrlevs: int = Field(ge=1, le=5)
    swintfl: Literal[0, 1]
    cofintflb: Optional[float] = Field(default=None, ge=0.01, le=10.0)
    expintflb: Optional[float] = Field(default=None, ge=0.1, le=1.0)
    swtopnrsrf: Optional[Literal[0, 1]] = None
    list_levelfluxes: Optional[ObjectList] = None

    @model_validator(mode='after')
    def _validate_drainfiltrationres(self) -> Self:
        if self.swintfl == 1:
            assert self.cofintflb is not None, 'cofintflb has to be provided if swintfl is 1.'
            assert self.expintflb is not None, 'expintflb has to be provided if swintfl is 1.'

        return self


class Flux(PySWAPBaseModel):
    """These objects are needed for the DrainageInfiltrationResitance class. Flux object should be 
    created for each level of drainage.

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

        table_datowltb (Table): date DATOWL [date] and channel water level LEVEL. Add suffix to the 
            dataframe headers according to the level number.
    """
    level_number: int = Field(exclude=True, ge=1, le=5)
    drares: float = Field(ge=10.0, le=1.0e5)
    infres: float = Field(ge=10.0, le=1.0e5)
    swallo: Literal[1, 2, 3]
    l: Optional[float] = Field(ge=1.0, le=1.0e5)
    zbotdr: float = Field(ge=-1000.0, le=0.0)
    swdtyp: Literal[1, 2]
    table_datowltb: Table

    @model_validator(mode='after')
    def _validate_flux(self) -> Self:
        if self.swallo == 1:
            assert self.l is not None, 'l has to be provided if swallo is 1.'

        return self

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


class DraFile(PySWAPBaseModel):
    """Main class representing the drainage file (.dra) for SWAP.

    Attributes:
        drfil (str): Name of the file.
        general (Any): General settings.
        fluxtable (Optional[Any]): Flux table.
        drainageformula (Optional[Any]): Drainage formula.
        drainageinfiltrationres (Optional[Any]): Drainage infiltration resistance.
    """

    drfil: str
    general: DraSettings = Field(exclude=True)
    fluxtable: Optional[DrainageFluxTable] = Field(default=None, exclude=True)
    drainageformula: Optional[DrainageFormula] = Field(
        default=None, exclude=True)
    drainageinfiltrationres: Optional[DrainageInfiltrationResitance] = Field(
        default=None, exclude=True)

    @property
    def content(self):
        return self._concat_sections()
