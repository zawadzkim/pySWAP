from dataclasses import dataclass, field
from pandas import DataFrame
from ..base.dtypes import Section, Subsection


@dataclass
class SurfaceFlow(Subsection):
    swpondmx: bool
    swrunon: bool
    rsro: float = 0.5
    rsroexp: float = 1.0
    pondmx: float | None = None
    rufil: str | None = None
    pondmxtb: DataFrame | None = None

    def __post_init__(self) -> None:

        if not self.swpondmx:
            assert self.pondmx is not None, "pondmx is required when swpondmx is False"
        else:
            assert self.pondmxtb is not None, "pondmxtb is required when swpondmx is True"

        if self.swrunon:
            assert self.rufil is not None, "runfil is required when swrunon is True"
