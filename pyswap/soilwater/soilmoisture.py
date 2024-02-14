from dataclasses import dataclass, field
from ..core.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class SoilMoisture(Subsection):
    """Soil moisture content and water balance."""

    swinco: int
    head_soildepth: DataFrame | None = None
    gwli: int | None = None
    inifil: str | None = None

    def __post_init__(self) -> None:

        if self.swinco not in range(1, 4):
            raise ValueError("swinco must be 1, 2, or 3")

        if self.swinco == 1:
            assert self.head_soildepth is not None, "head_soildepth is required when swinco is 1"

        elif self.swinco == 2:
            assert self.gwli is not None, "gwli is required when swinco is 2"

        else:
            assert self.inifil is not None, "inifil is required when swinco is 3"
