from typing import Optional, List
from ..core.utils.files import open_file
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from pydantic import computed_field, Field


class CropFile(PySWAPBaseModel):

    name: str
    path: str

    @computed_field(return_type=str)
    def content(self):
        return open_file(self.path, encoding='ascii')


class Crop(PySWAPBaseModel):
    """Holds the crop settings of the simulation."""

    swcrop: bool
    rds: Optional[float] = Field(default=None, ge=1, le=5000)
    croprotation: Optional[Table] = None
    cropfiles: Optional[List[CropFile]] = None

    def _validate_crop_section(self):
        if self.swcrop:
            assert self.rds is not None, "rds must be specified if swcrop is True"
            assert self.croprotation is not None, "croprotation must be specified if swcrop is True"

    def save_crop(self, path: str):
        return NotImplemented('Method not implemented yet')
