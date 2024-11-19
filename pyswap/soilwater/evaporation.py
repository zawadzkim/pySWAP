"""
Settings for evaporation.

Classes:
    Evaporation: Evaporation settings.
"""

from typing import Literal, Self

from pydantic import model_validator

from ..core import PySWAPBaseModel, SerializableMixin


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

        cfevappond (Optional[float]): hen ETref is used, evaporation
            coefficient in case of ponding.
        cfbs (Optional[float]): Coefficient for potential soil evaporation.
        rsoil (Optional[float]): Soil resistance of wet soil.
        cofredbl (Optional[float]): Soil evaporation coefficient of Black.
        rsigni (Optional[float]): Minimum rainfall to reset method of Black.
        cofredbo (Optional[float]): Soil evaporation coefficient of
            Boesten/Stroosnijder.
    """

    swcfbs: Literal[0, 1]
    swredu: Literal[0, 1, 2]
    cfevappond: float | None = None  # this is used if ETref is used
    cfbs: float | None = None
    rsoil: float | None = None
    cofredbl: float | None = None
    rsigni: float | None = None
    cofredbo: float | None = None

    @model_validator(mode="after")
    def _validate_evaporation(self) -> Self:
        if self.swcfbs:
            assert self.cfbs is not None, "cfbs is required when swcfbs is True"

        if self.swredu == 1:
            assert self.cofredbl is not None, "cofredbl is required when swredu is 1"
            assert self.rsigni is not None, "rsigni is required when swredu is 1"

        elif self.swredu == 2:
            assert self.cofredbo is not None, "cofredbo is required when swredu is 2"

        return self
