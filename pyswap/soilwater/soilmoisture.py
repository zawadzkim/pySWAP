from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from pydantic import model_validator
from typing import Literal, Optional


class SoilMoisture(PySWAPBaseModel):
    """Soil moisture content and water balance."""

    swinco: Literal[1, 2, 3]
    table_head_soildepth: Optional[Table] = None
    gwli: Optional[int] = None
    inifil: Optional[str] = None

    @model_validator(mode='after')
    def _validate_soil_moisture(self) -> None:

        if self.swinco == 1:
            assert self.table_head_soildepth is not None, "head_soildepth is required when swinco is 1"

        elif self.swinco == 2:
            assert self.gwli is not None, "gwli is required when swinco is 2"

        else:
            assert self.inifil is not None, "inifil is required when swinco is 3"
