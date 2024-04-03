from pandas import DataFrame
from ..core.utils.basemodel import PySWAPBaseModel
from pydantic import model_validator
from typing import Optional, Literal


class SurfaceFlow(PySWAPBaseModel):
    swpondmx: Literal[0, 1]
    swrunon: Literal[0, 1]
    rsro: float = 0.5
    rsroexp: float = 1.0
    pondmx: Optional[float] = None
    rufil: Optional[str] = None
    pondmxtb: Optional[DataFrame] = None

    @model_validator(mode='after')
    def _validate_surface_flow(self) -> None:

        if self.swpondmx == 0:
            assert self.pondmx is not None, "pondmx is required when swpondmx is 0"
        else:
            assert self.pondmxtb is not None, "pondmxtb is required when swpondmx is 1"

        if self.swrunon == 1:
            assert self.rufil is not None, "runfil is required when swrunon is 1"
