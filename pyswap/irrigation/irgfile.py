"""Create the irrigation file for the SWAP model.

Classes:
    IrrigationFile: The irrigation file.
"""

from pydantic import computed_field
from pandas import DataFrame, read_csv
from pyswap.core.utils.basemodel import PySWAPBaseModel


class IrrigationFile(PySWAPBaseModel):
    """The irrigation file.

    Attributes:
        name (str): The name of the file.
        path (str): The path to the file.
    """

    name: str
    path: str

    @computed_field(return_type=DataFrame)
    def content(self):
        return read_csv(self.path)
