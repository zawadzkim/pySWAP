"""
Plot groundwater levels (observed vs simulated) and compute the RMSE.
"""

import matplotlib.pyplot as plt
from pandas import DataFrame


def gwl(simulated: DataFrame, observed: DataFrame, title: str = 'Groundwater levels'):
    """Plot groundwater levels (observed vs simulated) and compute the RMSE.

    Parameters:
        simulated (DataFrame): Simulated groundwater levels
        observed (DataFrame): Observed groundwater levels
        title (str, optional): Title of the plot. Defaults to 'Groundwater levels'.
    """

    rmse = ((simulated - observed) ** 2).mean() ** 0.5

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(simulated, label='Simulated', color='black', linewidth=0.5)
    ax.plot(observed, label='Observed', marker='o',
            linestyle='None', markersize=2)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Groundwater level')
    ax.tick_params(axis='x', rotation=45)

    # add RMSE to the plot in the right lower corner
    ax.text(0.95, 0.05, f'RMSE: {rmse:.2f}', verticalalignment='bottom',
            horizontalalignment='right', transform=ax.transAxes)
    ax.legend()
    plt.tight_layout()
    plt.show()
