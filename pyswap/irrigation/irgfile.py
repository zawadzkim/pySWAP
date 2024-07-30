"""Create the irrigation file for the SWAP model.

Classes:
    IrrgFile: The irrigation file.
"""

from pydantic import Field
from pandas import read_csv
from ..core import PySWAPBaseModel, String, FileMixin
from pandas import DataFrame


class IrgFile(PySWAPBaseModel, FileMixin):
    """The irrigation file.

    Attributes:
        irgfil (str): the name of the irgfile without .irg extension.
        content (DataFrame): The content of the irrigation file.
    """

    irgfil: String
    content: DataFrame = Field(exclude=True)


def irg_from_csv(irgfil: str, path: str) -> IrgFile:
    """Load the irrigation file from a CSV file.

    Parameters:
        irgfil (str): the name of the irgfile without .irg extension.
        path (str): The path to the CSV file.

    Returns:
        IrgFile: The irrigation file.
    """
    return IrgFile(content=read_csv(path), irgfil=irgfil)
