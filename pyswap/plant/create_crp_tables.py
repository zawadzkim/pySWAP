"""Functions creating tables for the .CRP file."""
from pandas import DataFrame
import numpy as np


def create_gctb(lai: list) -> DataFrame:
    """Create the GCTB table.

    Arguments:
        lai: The leaf area index.

    Returns:
        DataFrame: The GCTB table.
    """
    dvs_values = np.linspace(0.0, 2.0, len(lai)).round(2)

    return DataFrame({'DVS': dvs_values, 'LAI': lai})


def create_chtb(chtb: dict) -> DataFrame:
    """Create the CHTB table.

    Arguments:
        chtb: The CHTB values.

    Returns:
        DataFrame: The CHTB table.
    """
    dvs_values = np.linspace(0.0, 2.0, len(chtb)).round(2)

    return DataFrame({'DVS': dvs_values, 'CH': chtb})


def create_rdtb(rdtb: list) -> DataFrame:
    """Create the RDTB table.

    Arguments:
        rdtb: The RDTB values.

    Returns:
        DataFrame: The RDTB table.
    """
    dvs_values = np.linspace(0.0, 2.0, len(rdtb)).round(2)

    return DataFrame({'DVS': dvs_values, 'RD': rdtb})


def create_kytb(kytb: list) -> DataFrame:
    """Create the KYTB table.

    Arguments:
        kytb: The KYTB values.

    Returns:
        DataFrame: The KYTB table.
    """
    dvs_values = np.linspace(0.0, 2.0, len(kytb)).round(2)

    return DataFrame({'DVS': dvs_values, 'KY': kytb})
