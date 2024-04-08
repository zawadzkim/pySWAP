"""Module for plotting evapotranspiration (potential vs actual)"""
import matplotlib.pyplot as plt
from pandas import DataFrame


def plot_evapotranspiration(potential: DataFrame, actual: DataFrame, title: str = 'Evapotranspiration'):
    """Plot evapotranspiration (potential vs actual) and compute the RMSE.

    Args:
        potential (DataFrame): Potential evapotranspiration
        actual (DataFrame): Actual evapotranspiration
        title (str, optional): Title of the plot. Defaults to 'Evapotranspiration'.
    """

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(potential, label='Potential', color='black', linewidth=0.5)
    ax.plot(actual, label='Actual', color='orange',
            linewidth=0.5, linestyle='--')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Evapotranspiration')
    ax.tick_params(axis='x', rotation=45)

    ax.legend()
    plt.tight_layout()
    plt.show()
