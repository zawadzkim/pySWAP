from typing import Optional, List, Literal
from typing_extensions import Self
from ..core import PySWAPBaseModel
from ..core import Table
from ..core import save_file
from .crpfile import *
from pydantic import Field


class Crop(PySWAPBaseModel):
    """Holds the crop settings of the simulation.

    Attributes:
        swcrop (int): Switch for crop:

            * 0 - Bare soil.
            * 1 - Simulate crop.

        rds (Optional[float]): Rooting depth of the crop [cm].
        table_croprotation (Optional[Table]): Table with crop rotation data.
        cropfiles (Optional[List[CropFile]]): List of crop files.

    Methods:
        write_crop: Write the crop files.
    """

    swcrop: Literal[0, 1]
    rds: Optional[float] = Field(default=None, ge=1, le=5000)
    table_croprotation: Optional[Table] = None
    cropfiles: Optional[List[CropFile]] = Field(default=None, exclude=True)

    def _validate_crop_section(self) -> Self:
        if self.swcrop == 1:
            assert self.rds is not None, "rds must be specified if swcrop is True"
            assert self.table_croprotation is not None, "croprotation must be specified if swcrop is True"

        return self

    def write_crop(self, path: str):
        count = 0
        for cropfile in self.cropfiles:
            count += 1
            save_file(
                string=cropfile.content,
                extension='crp',
                fname=cropfile.name,
                path=path
            )

        print(f'{count} crop file(s) saved.')
