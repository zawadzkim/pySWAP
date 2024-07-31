from ..core import Table, String
from ..core import PySWAPBaseModel, SerializableMixin
from pydantic import model_validator, field_validator
from typing import Optional, Literal
from typing_extensions import Self
from decimal import Decimal


class SurfaceFlow(PySWAPBaseModel, SerializableMixin):
    """Surface flow settings (ponding, runoff and runon).

    Attributes:
        swpondmx (Literal[0, 1]): Switch for variation ponding
            threshold for runoff

            * 0 - Ponding threshold for runoff is constant
            * 1 - Ponding threshold for runoff varies in time

        swrunon (Literal[0, 1]): Switch for runon

            * 0 - No runon
            * 1 - Use runon data

        rsro (Decimal): Drainage resistance for surface runoff
        rsroexp (Decimal): Exponent for drainage equation of surface runoff
        pondmx (Optional[Decimal]): In case of ponding, minimum
            thickness for runoff
        rufil (Optional[str]): Name of the runon file
        table_pondmxtb (Optional[Table]): Minimum thickness for runoff as
            a function of time
    """
    swpondmx: Literal[0, 1]
    swrunon: Literal[0, 1]
    rsro: Decimal = 0.5
    rsroexp: Decimal = 1.0
    pondmx: Optional[Decimal] = None
    rufil: Optional[String] = None
    table_pondmxtb: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_surface_flow(self) -> Self:

        if self.swpondmx == 0:
            assert self.pondmx is not None, \
                "pondmx is required when swpondmx is 0"
        else:
            assert self.table_pondmxtb is not None, \
                "pondmxtb is required when swpondmx is 1"

        if self.swrunon == 1:
            assert self.rufil is not None, \
                "runfil is required when swrunon is 1"

        return self

    @field_validator('rsro', 'rsroexp', 'pondmx')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.00'))
