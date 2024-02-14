from dataclasses import dataclass, field
from ..core.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class Evaporation(Subsection):
    swcfbs: bool
    swredu: int
    cfevappond: float | None = None  # this is used if ETref is used
    cfbs: float | None = None
    rsoil: float | None = None
    cofredbl: float | None = None
    rsigni: float | None = None
    cofredbo: float | None = None

    def __post_init__(self) -> None:

        if self.swcfbs:
            assert self.cfbs is not None, "cfbs is required when swcfbs is True"

        if self.swredu not in range(0, 3):
            raise ValueError("swredu must be 0, 1, or 2")

        if self.swredu == 1:
            assert self.cofredbl is not None, "cofredbl is required when swredu is 1"
            assert self.rsigni is not None, "rsigni is required when swredu is 1"

        elif self.swredu == 2:
            assert self.cofredbo is not None, "cofredbo is required when swredu is 2"
