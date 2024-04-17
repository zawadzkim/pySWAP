from typing import Optional, List, Literal, Any
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from ..core.utils.files import save_file, open_file
from .createcrop import *
from pydantic import computed_field, Field


class CropFile(PySWAPBaseModel):

    name: str = Field(exclude=True)
    path: Optional[str] = None
    prep: Optional[Any] = None
    cropdev_settings: Optional[Any] = None
    oxygenstress: Optional[Any] = None
    droughtstress: Optional[Any] = None
    saltstress: Optional[Any] = SaltStress(swsalinity=0)
    compensaterwu: Optional[Any] = CompensateRWUStress(swcompensate=0)
    interception: Optional[Any] = None
    scheduledirrigation: Optional[Any] = ScheduledIrrigation(schedule=0)

    def _concat_crp(self):
        string = ''
        for k, v in dict(self).items():
            if v is None or isinstance(v, str):
                continue
            string += v.model_string()
        return string

    @computed_field(return_type=str)
    def content(self):
        if self.path:
            return open_file(self.path)
        else:
            return self._concat_crp()


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
