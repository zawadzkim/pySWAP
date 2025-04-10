"""Interact with .csv files.

Functions:
    load_csv: Load a .csv file.
"""

from pathlib import Path

from pandas import DataFrame, read_csv


def load_csv(file: Path, delimiter=",", skiprows=None, index_col=None) -> DataFrame:
    """Load a .csv file.

    Arguments:
        file: Path to the .csv file.
    """
    if skiprows:
        return read_csv(
            file,
            delimiter=delimiter,
            skiprows=skiprows,
            index_col=index_col,
        )
    else:
        return read_csv(
            file,
            delimiter=delimiter,
            index_col=index_col,
        )
