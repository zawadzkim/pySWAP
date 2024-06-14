"""Loads data from the package resources."""
from importlib import resources
import pandas as pd

def load_csv(fname: str) -> pd.DataFrame:
    """Load a CSV file from the package resources.

    Args:
        file: Path to the file.

    Returns:
        DataFrame: Data from the CSV file.
    """
    return pd.read_csv(resources.open_text('pyswap.testcase.data', fname))


def load_txt(fname: str) -> str:
    """Load a text file from the package resources.

    Args:
        file: Path to the file.

    Returns:
        str: Data from the text file.
    """
    return resources.read_text('pyswap.testcase.data', fname)