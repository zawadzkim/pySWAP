from ..core.utils.files import open_file, save_file
from ..core.utils.basemodel import PySWAPBaseModel
from pydantic import computed_field, model_validator
from typing import Literal, Optional, Any


class DrainageFile(PySWAPBaseModel):

    name: str
    path: str

    @computed_field(return_type=str)
    def content(self):
        return open_file(self.path)


class LateralDrainage(PySWAPBaseModel):
    """Holds the lateral drainage settings of the simulation."""

    swdra: Literal[0, 1, 2]
    drfil: Optional[str] = None
    drainagefile: Optional[Any] = None

    @property
    def exclude(self) -> set:
        return {'drainagefile'}

    @model_validator(mode='after')
    def _validate_lateral_drainage(self):
        if self.swdra > 0:
            assert self.drfil is not None, "drfil is required when swdra is 1 or 2"

    def save_drainage(self, path: str):
        save_file(
            string=self.drainagefile.content,
            extension='dra',
            fname=self.drainagefile.name,
            path=path,
            mode='w'
        )
        return '.dra file saved successfully.'
