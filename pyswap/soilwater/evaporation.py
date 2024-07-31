"""
Settings for evaporation.

Classes:
    Evaporation: Evaporation settings.
"""

from ..core import PySWAPBaseModel, SerializableMixin
from typing import Literal, Optional
from typing_extensions import Self
from pydantic import model_validator, field_validator
from decimal import Decimal


class Evaporation(PySWAPBaseModel, SerializableMixin):
    """Evaporation settings.

    Attributes:
        swcfbs (int): Switch for use of soil factor CFBS to calculate Epot
        from ETref swredu (int): Switch for the method for reduction of
        potential soil evaporation:

            * 0 - reduction to maximum Darcy flux.
            * 1 - reduction to maximum Darcy flux and to maximum Black (1969).
            * 2 - reduction to maximum Darcy flux and to maximum
                Boesten/Stroosnijder (1986).

        cfevappond (Optional[Decimal]): hen ETref is used, evaporation
            coefficient in case of ponding.
        cfbs (Optional[Decimal]): Coefficient for potential soil evaporation.
        rsoil (Optional[Decimal]): Soil resistance of wet soil.
        cofredbl (Optional[Decimal]): Soil evaporation coefficient of Black.
        rsigni (Optional[Decimal]): Minimum rainfall to reset method of Black.
        cofredbo (Optional[Decimal]): Soil evaporation coefficient of
            Boesten/Stroosnijder.
    """
    swcfbs: Literal[0, 1]
    swredu: Literal[0, 1, 2]
    cfevappond: Optional[Decimal] = None  # this is used if ETref is used
    cfbs: Optional[Decimal] = None
    rsoil: Optional[Decimal] = None
    cofredbl: Optional[Decimal] = None
    rsigni: Optional[Decimal] = None
    cofredbo: Optional[Decimal] = None

    @model_validator(mode='after')
    def _validate_evaporation(self) -> Self:

        if self.swcfbs:
            assert self.cfbs is not None, \
                "cfbs is required when swcfbs is True"

        if self.swredu == 1:
            assert self.cofredbl is not None, \
                "cofredbl is required when swredu is 1"
            assert self.rsigni is not None, \
                "rsigni is required when swredu is 1"

        elif self.swredu == 2:
            assert self.cofredbo is not None, \
                "cofredbo is required when swredu is 2"

        return self

    @field_validator('cfevappond', 'cfbs', 'rsoil',
                     'cofredbl', 'rsigni', 'cofredbo')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.00'))
