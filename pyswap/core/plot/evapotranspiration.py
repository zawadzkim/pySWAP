import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def plot_evapotranspiration(potential: DataFrame, actual: DataFrame, title: str = 'Evapotranspiration'):
    """
    Plot evapotranspiration (potential vs actual) and compute the RMSE.

    Args:
        potential (DataFrame): DataFrame containing dates and values for potential evapotranspiration.
        actual (DataFrame): DataFrame containing dates and values for actual evapotranspiration.
        title (str, optional): Title of the plot. Defaults to 'Evapotranspiration'.
    """
    # Setting the visual context of the plot
    sns.set_context('poster')

    # Creating the plot
    fig, ax = plt.subplots(figsize=(34, 8))
    sns.lineplot(data=potential, ax=ax, label='Potential',
                 color='black', linewidth=1)
    sns.lineplot(data=actual, ax=ax, label='Actual',
                 color='orange', linewidth=1, linestyle='--')

    # Setting title and labels
    ax.set_title(title, pad=20)
    ax.set_xlabel('Date')
    ax.set_ylabel('Evapotranspiration')

    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    plt.tight_layout()
    plt.show()
