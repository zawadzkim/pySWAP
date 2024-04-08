from typing import Optional, Literal
from ..core.utils.basemodel import PySWAPBaseModel
from pydantic import model_validator


class SnowAndFrost(PySWAPBaseModel):

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: Optional[float] = None
    teprrain: Optional[float] = None
    teprsnow: Optional[float] = None
    snowcoef: Optional[float] = None
    tfrostst: Optional[float] = None
    tfrostend: Optional[float] = None

    @model_validator(mode='after')
    def _validate_snow_and_frost(self) -> None:

        if self.swsnow == 1:
            assert self.snowinco is not None, "snowinco is required when swsnow is True"
            assert self.teprrain is not None, "teprrain is required when swsnow is True"
            assert self.teprsnow is not None, "teprsnow is required when swsnow is True"
            assert self.snowcoef is not None, "snowcoef is required when swsnow is True"

        if self.swfrost == 1:
            assert self.tfrostst is not None, "tfrostst is required when swfrost is True"
            assert self.tfrostend is not None, "tfrostend is required when swfrost is True"
