"""
Settings for the Richards' equation with some reasonable defaults included.

Classes:
    RichardsSettings: Holds the settings for the Richards' equation.
"""

from ..core import PySWAPBaseModel, SerializableMixin
from typing import Literal
from decimal import Decimal
from pydantic import field_validator, Field


class RichardsSettings(PySWAPBaseModel, SerializableMixin):
    """Settings for the Richards' equation.

    Attributes:
        swkmean (int): Switch for averaging method of hydraulic conductivity
        swkimpl (Literal[0, 1]): Switch for updating hydraulic
            conductivity during iteration
        dtmin (Decimal): Minimum timestep
        dtmax (Decimal): Maximum timestep
        gwlconv (Decimal): Maximum difference of groundwater level between
            time steps
        critdevh1cp (Decimal): Maximum relative difference in pressure heads
            per compartment
        critdevh2cp (Decimal): Maximum absolute difference in pressure heads
            per compartment
        critdevponddt (Decimal): Maximum water balance error of ponding layer
        maxit (int): Maximum number of iteration cycles
        maxbacktr (int): Maximum number of back track cycles within
            an iteration cycle
    """

    swkmean: int
    swkimpl: Literal[0, 1]
    dtmin: Decimal = Field(default=Decimal('0.000001'),
                           ge=Decimal('0.0000001'), le=Decimal('0.1'))
    dtmax: Decimal = Field(default=Decimal(
        '0.04'), ge=Decimal('0.000001'), le=Decimal('1.0'))
    gwlconv: Decimal = Field(default=Decimal(
        '100.0'), ge=Decimal('0.00001'), le=Decimal('1000.0'))
    critdevh1cp: Decimal = Field(default=Decimal(
        '0.01'), ge=Decimal('0.0000000001'), le=Decimal('1000.0'))
    critdevh2cp: Decimal = Field(default=Decimal(
        '0.1'), ge=Decimal('0.0000000001'), le=Decimal('1000.0'))
    critdevponddt: Decimal = Field(default=Decimal(
        '0.0001'), ge=Decimal('0.000001'), le=Decimal('0.1'))
    maxit: int = Field(default=30, ge=5, le=100)
    maxbacktr: int = Field(default=3, ge=1, le=10)

    @field_validator('dtmin', 'dtmax', 'gwlconv',
                     'critdevh1cp', 'critdevh2cp', 'critdevponddt')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.0000000'))
