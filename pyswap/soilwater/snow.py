from typing import Optional, Literal
from ..core import PySWAPBaseModel, SerializableMixin
from pydantic import model_validator, field_validator
from typing_extensions import Self
from decimal import Decimal


class SnowAndFrost(PySWAPBaseModel, SerializableMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow
        snowinco (Optional[Decimal]): Initial snow water equivalent
        teprrain (Optional[Decimal]): Temperature above which all
            precipitation is rain
        teprsnow (Optional[Decimal]): Temperature below which all
            precipitation is snow
        snowcoef (Optional[Decimal]): Snowmelt calibration factor
        tfroststa (Optional[Decimal]): Soil temperature (oC) where reduction
            of water fluxes starts
        tfrostend (Optional[Decimal]): Soil temperature (oC) where reduction
            of water fluxes ends

    """

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: Optional[Decimal] = None
    teprrain: Optional[Decimal] = None
    teprsnow: Optional[Decimal] = None
    snowcoef: Optional[Decimal] = None
    tfrostst: Optional[Decimal] = None
    tfrostend: Optional[Decimal] = None

    @model_validator(mode='after')
    def _validate_snow_and_frost(self, v) -> Self:

        if self.swsnow == 1:
            assert self.snowinco is not None, \
                "snowinco is required when swsnow is True"
            assert self.teprrain is not None, \
                "teprrain is required when swsnow is True"
            assert self.teprsnow is not None, \
                "teprsnow is required when swsnow is True"
            assert self.snowcoef is not None, \
                "snowcoef is required when swsnow is True"

        if self.swfrost == 1:
            assert self.tfrostst is not None, \
                "tfrostst is required when swfrost is True"
            assert self.tfrostend is not None, \
                "tfrostend is required when swfrost is True"

        return self

    @field_validator('snowinco', 'teprrain', 'teprsnow', 'snowcoef',
                     'tfrostst', 'tfrostend')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.00'))
