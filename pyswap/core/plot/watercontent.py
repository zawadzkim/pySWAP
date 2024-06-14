from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def water_content(df_vap: pd.DataFrame, title: str = 'Water content'):
    """Plot water content as heatmap with time on the x-axis and depth on the y-axis.

    Parameters:
        df_vap (pd.DataFrame): DataFrame containing the water content data
        title (str, optional): Title of the plot. Defaults to 'Water content'.
    """
    sns.set_context('poster')

    df_wcont = df_vap[['depth', 'date', 'wcontent']]
    df_wcont['date'] = pd.to_datetime(
        df_wcont['date'])
    df_wcont['date'] = df_wcont['date'].dt.strftime('%Y-%m')
    df_wcont['depth'] = df_wcont['depth'].astype(float)
    df_wcont['wcontent'] = df_wcont['wcontent'].astype(float)
    pivot_table = df_wcont.pivot(
        columns='date', index='depth', values='wcontent')

    pivot_table.sort_index(ascending=True, inplace=True)
    plt.figure(figsize=(34, 8))
    ax = sns.heatmap(pivot_table, cmap="YlGnBu")
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Depth (cm)')

    plt.gca().invert_yaxis()

    plt.xticks(rotation=45)
    plt.tight_layout(pad=20)
    plt.show()
