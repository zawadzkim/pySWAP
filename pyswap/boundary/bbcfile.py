"""
Bottom boundary condition settings for the SWAP model.

Classes:
    BottomBoundary: Holds the settings of the bottom boundary conditions of
    the .swp file.
"""
from .base import BottomBoundaryBase
from ..core import FileMixin


class BBCFile(BottomBoundaryBase, FileMixin):
    """Bottom boundary file.

    All attributes are the same as in the BottomBOundaryBase. There
    is an additional property allowing to save the content to a file.
    """
