from typing import Literal, Self

from ..core import PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin


class SnowAndFrost(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow
        snowinco (Optional[float]): Initial snow water equivalent
        teprrain (Optional[float]): Temperature above which all
            precipitation is rain
        teprsnow (Optional[float]): Temperature below which all
            precipitation is snow
        snowcoef (Optional[float]): Snowmelt calibration factor
        tfroststa (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes starts
        tfrostend (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes ends

    """

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: float | None = None
    teprrain: float | None = None
    teprsnow: float | None = None
    snowcoef: float | None = None
    tfrostst: float | None = None
    tfrostend: float | None = None
