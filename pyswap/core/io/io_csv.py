"""Interact with .csv files.

Functions:
    load_csv: Load a .csv file.
"""

from pathlib import Path

from pandas import DataFrame, read_csv


def load_csv(file: Path) -> DataFrame:
    """Load a .csv file.

    Arguments:
        file: Path to the .csv file.
    """

    return read_csv(file)
