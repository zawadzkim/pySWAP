"""
drafile.py contains classes that compose the .dra file for SWAP.

"""
from pyswap.core.utils.basemodel import PySWAPBaseModel
from pyswap.core.utils.fields import FloatList, Table, ObjectList
from pyswap.core.utils.valueranges import UNITRANGE
from pyswap.core.utils.files import open_file
from pydantic import Field, model_validator, computed_field
from typing import Literal, Optional, Any


class DraFile(PySWAPBaseModel):

    name: str = Field(exclude=True)
    path: Optional[str] = None
    general: Any
    fluxtable: Optional[Any] = None
    drainageformula: Optional[Any] = None
    drainageinfiltrationres: Optional[Any] = None

    @computed_field(return_type=str)
    def content(self):
        if self.path:
            return open_file(self.path)
        else:
            return self._concat_sections()


class DraSettings(PySWAPBaseModel):
    dramet: Literal[1, 2, 3]
    swdivd: Literal[1, 2]
    cofani: Optional[FloatList]
    swdislay: Literal[0, 2, 3, '-']

    # @model_validator(mode='after')
    # def _validate_drasettings(self):
    #     if


class DrainageFluxTable(PySWAPBaseModel):
    lm1: float = Field(ge=1.0, le=1000.0)
    table_qdrntb: Table


class DrainageFormula(PySWAPBaseModel):
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
    def _validate_settings(self):
        if self.ipos in [3, 4, 5]:
            assert self.khbot is not None, 'khbot has to be provided if IPOS is 3.'
            assert self.zintf is not None, 'zintf has to be provided if IPOS is 3.'
        if self.ipos in [4, 5]:
            assert self.kvtop is not None, 'kvtop has to be provided if IPOS is 3.'
            assert self.kvbot is not None, 'kvbot has to be provided if IPOS is 3.'
        if self.ipos == 5:
            assert self.geofac is not None, 'geofac has to be provided if IPOS is 3.'


class DrainageInfiltrationResitance(PySWAPBaseModel):
    nrlevs: int = Field(ge=1, le=5)
    swintfl: Literal[0, 1]
    cofintflb: float = Field(ge=0.01, le=10.0)
    expintflb: float = Field(ge=0.1, le=1.0)
    swtopnrsrf: Literal[0, 1]
    list_levelfluxes: ObjectList

    @model_validator(mode='after')
    def _validate_settings(self):
        if self.swintfl == 1:
            assert self.cofintflb is not None, 'cofintflb has to be provided if swintfl is 1.'
            assert self.expintflb is not None, 'expintflb has to be provided if swintfl is 1.'


class Flux(PySWAPBaseModel):
    level_number: int = Field(exclude=True, ge=1, le=5)
    drares: float = Field(ge=10.0, le=1.0e5)
    infres: float = Field(ge=10.0, le=1.0e5)
    swallo: Literal[1, 2]
    l: Optional[float] = Field(ge=1.0, le=1.0e5)
    zbotdr: float = Field(ge=-1000.0, le=0.0)
    swdtyp: Literal[1, 2]
    table_datowltb: Table

    @model_validator(mode='after')
    def _validate_settings(self):
        if self.swallo == 1:
            assert self.l is not None, 'l has to be provided if swallo is 1.'

    def model_dump(self, **kwargs):
        # Call the super method to get the dictionary representation.
        d = super().model_dump(**kwargs)

        # If level_number is set, modify the key names.
        if self.level_number is not None:
            new_d = {}
            suffix = str(self.level_number)
            for key, value in d.items():
                new_d[key + suffix] = value
            return new_d
        return d
