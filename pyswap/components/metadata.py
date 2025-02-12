"""Model metadata.

Classes:
    Metadata: Metadata of a SWAP model.
"""

from pydantic import Field

from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String
from pyswap.utils.mixins import SerializableMixin


class Metadata(PySWAPBaseModel, SerializableMixin):
    """Metadata of a SWAP model.

    Metadata is intended more as a modelling exercise metadata than a model
    metadata. You should create one Metadata object at the beginning of your
    model script and pass it to all Model objects you create in between. It is
    used to describe model runs if they are stored in a database. Only `project`
    is passed to the swap file.

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
