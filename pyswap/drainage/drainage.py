"""
Lateral drainage settings.

Classes:
    Drainage: The lateral drainage settings.
"""
from ..core import PySWAPBaseModel, save_file
from pydantic import model_validator, Field
from typing import Literal, Optional, Any


class Drainage(PySWAPBaseModel):
    """The lateral drainage settings of the simulation.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.
        drfil (Optional[str]): Name of the drainage file.
        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: Literal[0, 1, 2]
    drfil: Optional[str] = None
    drafile: Optional[Any] = Field(default=None, exclude=True)

    @model_validator(mode='after')
    def _validate_drainage(self):
        if self.swdra > 0:
            assert self.drfil is not None, "drfil is required when swdra is 1 or 2"
            assert self.drafile is not None, "drafile is required when swdra is 1 or 2"

    def write_dra(self, path: str):
        save_file(
            string=self.drafile.content,
            extension='dra',
            fname=self.drafile.drfil,
            path=path
        )

        print(f'{self.drfil}.dra saved.')
