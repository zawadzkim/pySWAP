"""Script for Part 0: Preparation, Sowing, Germination and Harvest
TODO: Replace everywhere the property I made for excluding the fields with Field(exclude=True)!!
TODO: Would be great to have the dependency of paramteres included in the definition of the Field objects.
"""

from ...core.utils.basemodel import PySWAPBaseModel
from typing import Literal, Optional
from pydantic import Field, model_validator


class Preparation(PySWAPBaseModel):
    swprep: Literal[0, 1]
    swsow: Literal[0, 1]
    swgerm: Literal[0, 1, 2]
    swharv: Literal[0, 1]
    dvsend: float = Field(ge=0.0, le=3.0)
    zprep: Optional[float] = Field(default=None, ge=-100.0, le=0.0)
    hprep: Optional[float] = Field(default=None, ge=-200.0, le=0.0)
    maxprepdelay: Optional[int] = Field(default=None, ge=1, le=366)
    zsow: Optional[float] = Field(default=None, ge=-100.0, le=0.0)
    hsow: Optional[float] = Field(default=None, ge=-200.0, le=0.0)
    ztempsow: Optional[float] = Field(default=None,  ge=-100.0, le=0.0)
    tempsow: Optional[float] = Field(default=None, ge=0.0, le=30.0)
    maxsowdelay: Optional[int] = Field(default=None, ge=1, le=366)
    tsumemopt: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    tbasem: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    teffmx: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    hdrgerm: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    hwetgerm: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    zgerm: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    agerm: Optional[float] = Field(default=None, ge=0.0, le=1000.0)

    @model_validator(mode='after')
    def _validate_prepartion(self):
        if self.swprep == 1:
            assert self.zprep is not None, "zprep is required when swprep is 1."
            assert self.hprep is not None, "hprep is required when swprep is 1."
            assert self.maxprepdelay is not None, "maxprepdelay is required when swprep is 1."

        if self.swsow == 1:
            assert self.zsow is not None, "zsow is required when swsow is 1."
            assert self.hsow is not None, "hsow is required when swsow is 1."
            assert self.ztempsow is not None, "ztempsow is required when swsow is 1."
            assert self.tempsow is not None, "tempsow is required when swsow is 1."
            assert self.maxsowdelay is not None, "maxsowdelay is required when swsow is 1."

        if self.swgerm in (1, 2):
            assert self.tsumemeopt is not None, "tsumemeopt is required when swgerm is 1 or 2."
            assert self.tbasem is not None, "tbasem is required when swgerm is 1 or 2."
            assert self.teffmx is not None, "teffmx is required when swgerm is 1 or 2."
        elif self.swgerm == 2:
            assert self.hdrygerm is not None, "hdrygerm is required when swgerm is 2."
            assert self.hwetgerm is not None, "hwetgerm is required when swgerm is 2."
            assert self.zgerm is not None, "zgerm is required when swgerm is 2."
            assert self.agerm is not None, "agerm is required when swgerm is 2."
