from typing import Optional
from ..core.utils.basemodel import Section, Subsection, PySWAPBaseModel
from pandas import DataFrame
from pydantic import model_validator


class SnowAndFrost(PySWAPBaseModel):

    swsnow: bool
    swfrost: bool
    snowinco: Optional[float] = None
    teprrain: Optional[float] = None
    teprsnow: Optional[float] = None
    snowcoef: Optional[float] = None
    tfrostst: Optional[float] = None
    tfrostend: Optional[float] = None

    @model_validator(mode='after')
    def _validate_snow_and_frost(self) -> None:

        if self.swsnow:
            assert self.snowinco is not None, "snowinco is required when swsnow is True"
            assert self.teprrain is not None, "teprrain is required when swsnow is True"
            assert self.teprsnow is not None, "teprsnow is required when swsnow is True"
            assert self.snowcoef is not None, "snowcoef is required when swsnow is True"

        if self.swfrost:
            assert self.tfrostst is not None, "tfrostst is required when swfrost is True"
            assert self.tfrostend is not None, "tfrostend is required when swfrost is True"
