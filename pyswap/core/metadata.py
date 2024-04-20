"""
metadata.py contains the Metadata class collecting basic information about the model.
"""

from .utils.basemodel import PySWAPBaseModel
from typing import Optional
from pydantic import Field


class Metadata(PySWAPBaseModel):
    """Metadata of a SWAP model."""

    author: str = Field(exclude=True)
    institution: str = Field(exclude=True)
    email: str = Field(exclude=True)
    project: str
    swap_ver: str = Field(exclude=True)
    comment: Optional[str] = Field(default=None, exclude=True)
