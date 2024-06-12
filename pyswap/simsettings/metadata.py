"""
Metadata class collecting basic information about the model.

Classes:
    Metadata: Metadata of a SWAP model.
"""

from ..core import PySWAPBaseModel
from typing import Optional
from pydantic import Field


class Metadata(PySWAPBaseModel):
    """Metadata of a SWAP model.

    Attributes:
        author (str): Author of the model.
        institution (str): Institution of the author.
        email (str): Email of the author.
        project (str): Name of the project.
        swap_ver (str): Version of SWAP used.
        comment (Optional[str]): Comment about the model.
    """

    author: str = Field(exclude=True)
    institution: str = Field(exclude=True)
    email: str = Field(exclude=True)
    project: str
    swap_ver: str = Field(exclude=True)
    comment: Optional[str] = Field(default=None, exclude=True)
