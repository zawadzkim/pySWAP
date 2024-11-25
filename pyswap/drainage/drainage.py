"""
Lateral drainage settings.

Classes:
    Drainage: The lateral drainage settings.
"""

from typing import Literal, Self

from pydantic import Field, model_validator

from ..core import PySWAPBaseModel
from ..core.mixins import ComplexSerializableMixin, YAMLValidatorMixin
from .drafile import DraFile


class Drainage(PySWAPBaseModel, ComplexSerializableMixin, YAMLValidatorMixin):
    """The lateral drainage settings of the simulation.

    Attributes:
        swdra (Literal[0, 1, 2]): Switch for lateral drainage.

            * 0 - No drainage.
            * 1 - Simulate with a basic drainage routine.
            * 2 - Simulate with surface water management.

        drafile (Optional[Any]): Content of the drainage file.
    """

    swdra: Literal[0, 1, 2]
    drafile: DraFile | None = Field(default=None)

    @property
    def dra(self):
        return self.concat_nested_models(self.drafile)

    def write_dra(self, path: str):
        self.drafile.save_file(
            string=self.dra, extension="dra", fname=self.drafile.drfil, path=path
        )

        print('dra file saved.')
