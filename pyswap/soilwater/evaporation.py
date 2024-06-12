from ..core import PySWAPBaseModel
from typing import Literal, Optional
from pydantic import model_validator


class Evaporation(PySWAPBaseModel):
    swcfbs: Literal[0, 1]
    swredu: Literal[0, 1, 2]
    cfevappond: Optional[float] = None  # this is used if ETref is used
    cfbs: Optional[float] = None
    rsoil: Optional[float] = None
    cofredbl: Optional[float] = None
    rsigni: Optional[float] = None
    cofredbo: Optional[float] = None

    @model_validator(mode='after')
    def _validate_evaporation(self) -> None:

        if self.swcfbs:
            assert self.cfbs is not None, "cfbs is required when swcfbs is True"

        if self.swredu == 1:
            assert self.cofredbl is not None, "cofredbl is required when swredu is 1"
            assert self.rsigni is not None, "rsigni is required when swredu is 1"

        elif self.swredu == 2:
            assert self.cofredbo is not None, "cofredbo is required when swredu is 2"
