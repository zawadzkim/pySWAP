from .base import BottomBoundaryBase
from .bbcfile import BBCFile

"""
Bottom boundary condition settings for the SWAP model.

Classes:
    BottomBoundary: Holds the settings of the bottom boundary conditions of
        the .swp file.
"""
from typing import Literal


class BottomBoundary(BottomBoundaryBase):
    """Bottom boundary condition settings in the swp file.

    Attributes:
        swbbcfile (Literal[0, 1]): Switch for file with bottom boundary data:

            * 0 - data are specified in current file
            * 1 - data are specified in separate file


        bbcfile (Optional[BBCFile]): the BBCFile object.
    """

    swbbcfile: Literal[0, 1]
    bbcfile: BBCFile | None = None

    @property
    def bbc(self):
        return "".join(self.bbcfile.concat_attributes())

    def write_bbc(self, path: str):
        self.bbcfile.save_file(
            string=self.bbc, extension="bbc", fname=self.bbcfil, path=path
        )
