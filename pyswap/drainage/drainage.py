"""
drainage.py contains the Lateral drainage settings.

"""
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.files import save_file
from pydantic import model_validator, Field
from typing import Literal, Optional, Any


class LateralDrainage(PySWAPBaseModel):
    """Holds the lateral drainage settings of the simulation."""

    swdra: Literal[0, 1, 2]
    drfil: Optional[str] = None
    drainagefile: Optional[Any] = Field(default=None, exclude=True)

    @model_validator(mode='after')
    def _validate_lateral_drainage(self):
        if self.swdra > 0:
            assert self.drfil is not None, "drfil is required when swdra is 1 or 2"
            assert self.drainagefile is not None, "drainagefile is required when swdra is 1 or 2"

    def write_dra(self, path: str):
        save_file(
            string=self.drainagefile.content,
            extension='dra',
            fname=self.drfil,
            path=path
        )

        print(f'{self.drfil}.dra saved.')
