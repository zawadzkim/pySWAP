"""
## Metadata

Classes:
    Metadata: Metadata of a SWAP model.
"""

from pydantic import Field

from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import SerializableMixin
from pyswap.core.fields import String

__all__ = ["Metadata"]


class Metadata(PySWAPBaseModel, SerializableMixin):
    """Metadata of a SWAP model.

    Attributes:
        author (str): Author of the model.
        institution (str): Institution of the author.
        email (str): Email of the author.
        project (str): Name of the project.
        swap_ver (str): Version of SWAP used.
        comment (Optional[str]): Comment about the model.
    """

    author: String = Field(exclude=True)
    institution: String = Field(exclude=True)
    email: String = Field(exclude=True)
    project: String
    swap_ver: String = Field(exclude=True)
    comment: String | None = Field(default=None, exclude=True)
