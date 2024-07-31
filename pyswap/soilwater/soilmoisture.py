from ..core import PySWAPBaseModel, SerializableMixin
from ..core import Table, String
from pydantic import model_validator, field_validator
from typing import Literal, Optional
from typing_extensions import Self
from decimal import Decimal


class SoilMoisture(PySWAPBaseModel, SerializableMixin):
    """Soil moisture content and water balance.

    !!! warning
        swinco = 3 is not yet implemented. The model will run, but the output
        will not be retrieved.

    Attributes:
        swinco (int): Switch for the type of initial soil moisture condition:

            * 1 - pressure head as function of soil depth.
            * 2 - pressure head of each compartment is in
                hydrostatic equilibrium with initial groundwater level.
            * 3 - read final pressure heads from output file of previous
                Swap simulation.

        table_head_soildepth (Optional[Table]): Table with head and
            soil depth data.
        gwli (Optional[Decimal]): Initial groundwater level [cm].
        inifil (Optional[str]): name of output file *.END which contains
            initial values.
    """

    swinco: Literal[1, 2, 3]
    table_head_soildepth: Optional[Table] = None
    gwli: Optional[Decimal] = None
    inifil: Optional[String] = None

    @model_validator(mode='after')
    def _validate_soil_moisture(self) -> Self:

        if self.swinco == 1:
            assert self.table_head_soildepth is not None, \
                "head_soildepth is required when swinco is 1"

        elif self.swinco == 2:
            assert self.gwli is not None, "gwli is required when swinco is 2"

        else:
            assert self.inifil is not None, \
                "inifil is required when swinco is 3"

        return self

    @field_validator('gwli')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.00'))
