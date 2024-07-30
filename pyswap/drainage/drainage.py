"""
Lateral drainage settings.

Classes:
    Drainage: The lateral drainage settings.
"""
from ..core import PySWAPBaseModel
from ..core.mixins import ComplexSerializableMixin
from pydantic import model_validator, Field
from typing import Literal, Optional
from typing_extensions import Self
from .drafile import DraFile


class Drainage(PySWAPBaseModel, ComplexSerializableMixin):
    """The lateral drainage settings of the simulation.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0 - No drainage.
            * 1 - Simulate with a basic drainage routine.
            * 2 - Simulate with surface water management.

        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: Literal[0, 1, 2]
    drafile: Optional[DraFile] = Field(default=None)

    @property
    def dra(self):
        return self.concat_nested_models(self.drafile)

    @model_validator(mode='after')
    def _validate_drainage(self) -> Self:
        if self.swdra > 0:
            assert self.drafile is not None, \
                "drafile is required when swdra is 1 or 2"

        return self

    def write_dra(self, path: str):
        self.drafile.save_file(
            string=self.dra,
            extension='dra',
            fname=self.drafile.drfil,
            path=path
        )
