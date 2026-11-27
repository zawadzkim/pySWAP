"""Plot evapotranspiration (potential vs actual)."""

import matplotlib.pyplot as plt
from pandas import DataFrame

from pyswap.core.plot._style import POSTER


def evapotranspiration(
    potential: DataFrame, actual: DataFrame, title: str = "Evapotranspiration"
):
    """Plot evapotranspiration (potential vs actual).

    Paremeters:
        potential (DataFrame): DataFrame containing dates and values for potential evapotranspiration.
        actual (DataFrame): DataFrame containing dates and values for actual evapotranspiration.
        title (str, optional): Title of the plot. Defaults to 'Evapotranspiration'.
    """

    with plt.rc_context(POSTER):
        _fig, ax = plt.subplots(figsize=(34, 8))
        ax.plot(potential, label="Potential", color="black", linewidth=1)
        ax.plot(actual, label="Actual", color="orange", linewidth=1, linestyle="--")

        ax.set_title(title, pad=20)
        ax.set_xlabel("Date")
        ax.set_ylabel("Evapotranspiration")

        ax.tick_params(axis="x", rotation=45)
        ax.legend()
        plt.tight_layout()
        plt.show()
