from typing import Optional, List, Literal
from typing_extensions import Self
from ..core import PySWAPBaseModel, SerializableMixin, Table, save_file
from .crpfile import CropFile
from pydantic import Field, field_validator, model_validator
from decimal import Decimal


class Crop(PySWAPBaseModel, SerializableMixin):
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
    rds: Optional[Decimal] = Field(default=None, ge=1, le=5000)
    table_croprotation: Optional[Table] = None
    cropfiles: Optional[List[CropFile]] = Field(default=None, exclude=True)

    @model_validator(mode='after')
    def _validate_crop_section(self) -> Self:
        if self.swcrop == 1:
            assert self.rds is not None, \
                "rds must be specified if swcrop is True"
            assert self.table_croprotation is not None, \
                "croprotation must be specified if swcrop is True"

        return self

    @field_validator('rds')
    def set_decimals(cls, v):
        return v.quantize(Decimal('0.00'))

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
