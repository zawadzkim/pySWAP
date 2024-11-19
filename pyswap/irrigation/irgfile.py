"""Create the irrigation file for the SWAP model.

Classes:
    IrrgFile: The irrigation file.
"""

from pandas import DataFrame, read_csv
from pydantic import Field

from ..core import FileMixin, PySWAPBaseModel, String


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
