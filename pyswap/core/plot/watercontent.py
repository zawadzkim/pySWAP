"""module for plotting water content as heatmap with time on the x-axis and depth on the y-axis"""

from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def plot_wcontent(df_vap: pd.DataFrame, title: str = 'Water content'):
    """Plot water content as heatmap with time on the x-axis and depth on the y-axis.

    Args:
        df_vap (pd.DataFrame): DataFrame containing the water content data
        title (str, optional): Title of the plot. Defaults to 'Water content'.
    """

    df_wcont = df_vap[['depth', 'date', 'wcontent']]
    df_wcont['date'] = pd.to_datetime(df_wcont['date'])
    df_wcont['depth'] = df_wcont['depth'].astype(float)
    df_wcont['wcontent'] = df_wcont['wcontent'].astype(float)
    pivot_table = df_wcont.pivot(
        columns='date', index='depth', values='wcontent')

    pivot_table.sort_index(ascending=True, inplace=True)

    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(pivot_table, cmap="YlGnBu")
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Depth')

    plt.gca().invert_yaxis()

    ax.set_xticklabels([pd.to_datetime(tm).strftime('%Y-%m')
                       for tm in pivot_table.columns])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
