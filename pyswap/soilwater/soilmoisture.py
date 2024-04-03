from dataclasses import dataclass, field
from ..core.utils.basemodel import Section, Subsection, PySWAPBaseModel
from pandas import DataFrame
from pydantic import model_validator
from typing import Literal, Optional


class SoilMoisture(PySWAPBaseModel):
    """Soil moisture content and water balance."""

    swinco: Literal[1, 2, 3]
    head_soildepth: Optional[DataFrame] = None
    gwli: Optional[int] = None
    inifil: Optional[str] = None

    @model_validator(mode='after')
    def _validate_soil_moisture(self) -> None:

        if self.swinco == 1:
            assert self.head_soildepth is not None, "head_soildepth is required when swinco is 1"

        elif self.swinco == 2:
            assert self.gwli is not None, "gwli is required when swinco is 2"

        else:
            assert self.inifil is not None, "inifil is required when swinco is 3"
