"""Create the irrigation file for the SWAP model.

Classes:
    IrrigationFile: The irrigation file.
"""

from pydantic import Field, validator
from pandas import read_csv
from ..core import PySWAPBaseModel, irrigation_schema
from pandas import DataFrame


class IrgFile(PySWAPBaseModel):
    """The irrigation file.

    Attributes:
        irgfil (str): the name of the irgfile without .irg extension.
        content (Table): The content of the irrigation file.
    """

    irgfil: str
    content: DataFrame = Field(exclude=True)

    @validator('content')
    def _validate_content(cls, v):
        try:
            validated = irrigation_schema.validate(v)
            return validated
        except Exception as e:
            raise ValueError(f"Invalid irrigation schema: {e}")


def irg_from_csv(irgfil: str, path: str) -> IrgFile:
    """Load the irrigation file from a CSV file.

    Parameters:
        irgfil (str): the name of the irgfile without .irg extension.
        path (str): The path to the CSV file.

    Returns:
        IrgFile: The irrigation file.
    """
    return IrgFile(content=read_csv(path), irgfil=irgfil)
