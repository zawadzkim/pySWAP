from dataclasses import dataclass, field
from ..core.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class SnowAndFrost(Subsection):

    swsnow: bool
    swfrost: bool
    snowinco: float | None = None
    teprrain: float | None = None
    teprsnow: float | None = None
    snowcoef: float | None = None
    tfrostst: float | None = None
    tfrostend: float | None = None

    def __post_init__(self) -> None:

        if self.swsnow:
            assert self.snowinco is not None, "snowinco is required when swsnow is True"
            assert self.teprrain is not None, "teprrain is required when swsnow is True"
            assert self.teprsnow is not None, "teprsnow is required when swsnow is True"
            assert self.snowcoef is not None, "snowcoef is required when swsnow is True"

        if self.swfrost:
            assert self.tfrostst is not None, "tfrostst is required when swfrost is True"
            assert self.tfrostend is not None, "tfrostend is required when swfrost is True"
