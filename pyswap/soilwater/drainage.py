from ..core.utils.files import open_file
from ..core.utils.basemodel import PySWAPBaseModel
from pydantic import computed_field, model_validator
from typing import Literal, Optional


class DrainageFile(PySWAPBaseModel):

    name: str
    path: str

    @computed_field(return_type=str)
    def content(self):
        return open_file(self.path, encoding='ascii')


class LateralDrainage(PySWAPBaseModel):
    """Holds the lateral drainage settings of the simulation."""

    swdra: Literal[0, 1, 2]
    drfil: Optional[str] = None

    @model_validator(mode='after')
    def _validate_lateral_drainage(self):
        if self.swdra > 0:
            assert self.drfil is not None, "drfil is required when swdra is 1 or 2"

    def save_drainage(self, path: str):
        return NotImplemented('Method not implemented yet')
