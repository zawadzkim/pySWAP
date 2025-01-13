"""
Functions:
    water_content: Plot water content as heatmap.
"""

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def water_content(
    df: pd.DataFrame,
    depth_col: str,
    date_col: str,
    wcontent_col: str,
    title: str = "Water content",
):
    """Plot water content as heatmap.

    For this function to work, the user should either use the `vap` output
    converted to a dataframe, or make sure that in the csv_tz output they
    provide, only the water content data is present.

    Parameters:
        df (pd.DataFrame): DataFrame containing the water content data
        depth_col (str): Column name for depth data
        date_col (str): Column name for date data
        wcontent_col (str): Column name for water content data
        title (str, optional): Title of the plot. Defaults to 'Water content'.
    """

    sns.set_context("poster")

    df_wcont = df_vap[["depth", "date", "wcontent"]]
    df_wcont["date"] = pd.to_datetime(df_wcont["date"])
    df_wcont["date"] = df_wcont["date"].dt.strftime("%Y-%m")
    df_wcont["depth"] = df_wcont["depth"].astype(float)
    df_wcont["wcontent"] = df_wcont["wcontent"].astype(float)
    pivot_table = df_wcont.pivot(columns="date", index="depth", values="wcontent")

    pivot_table.sort_index(ascending=True, inplace=True)
    plt.figure(figsize=(34, 8))
    ax = sns.heatmap(pivot_table, cmap="YlGnBu")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Depth (cm)")

    plt.gca().invert_yaxis()

    plt.xticks(rotation=45)
    plt.tight_layout(pad=20)
    plt.show()
