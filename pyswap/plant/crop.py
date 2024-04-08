from typing import Optional, List, Literal
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from ..core.utils.files import save_file, open_file
from pydantic import computed_field, Field


class CropFile(PySWAPBaseModel):

    name: str
    path: str

    @computed_field(return_type=str)
    def content(self):
        return open_file(self.path)


class Crop(PySWAPBaseModel):
    """Holds the crop settings of the simulation."""

    swcrop: Literal[0, 1]
    rds: Optional[float] = Field(default=None, ge=1, le=5000)
    table_croprotation: Optional[Table] = None
    cropfiles: Optional[List[CropFile]] = None

    @property
    def exclude(self) -> set:
        return {'cropfiles'}

    def _validate_crop_section(self):
        if self.swcrop == 1:
            assert self.rds is not None, "rds must be specified if swcrop is True"
            assert self.table_croprotation is not None, "croprotation must be specified if swcrop is True"

    def save_crop(self, path: str):
        count = 0
        for cropfile in self.cropfiles:
            count += 1
            save_file(
                string=cropfile.content,
                extension='crp',
                fname=cropfile.name,
                path=path,
                mode='w'
            )
        return f'{count} crop file(s) saved successfully.'
