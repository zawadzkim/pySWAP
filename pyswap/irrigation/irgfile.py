"""Create the irrigation file for the SWAP model.

Classes:
    IrrigationFile: The irrigation file.
"""

from pydantic import Field
from pandas import read_csv
from ..core import PySWAPBaseModel
from pandas import DataFrame


class IrgFile(PySWAPBaseModel):
    """The irrigation file.

    !!! warning
        The irrigation file is the first to have pandera validation. However, 
        it is not yet complete. Some columns are set to non-required, but they
        might be required if solute transport is used.

    Attributes:
        irgfil (str): the name of the irgfile without .irg extension.
        content (DataFrame): The content of the irrigation file.
    """

    irgfil: str
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
