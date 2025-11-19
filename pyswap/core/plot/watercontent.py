# mypy: disable-error-code="attr-defined"
# For some reason, the error was raised on the definition of month labels based
# on pivot table columns (which are dates). Error disabled for now. We will see
# if any bugs come up.

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

    df_wcont = df[[depth_col, date_col, wcontent_col]]

    df_wcont.loc[:, date_col] = pd.to_datetime(df_wcont[date_col])
    df_wcont.loc[:, depth_col] = df_wcont[depth_col].astype(float)
    df_wcont.loc[:, wcontent_col] = df_wcont[wcontent_col].astype(float)

    pivot_table = df_wcont.pivot(columns=date_col, index=depth_col, values=wcontent_col)
    pivot_table = pivot_table.sort_index(axis=1)

    plt.figure(figsize=(34, 8))
    sns.heatmap(pivot_table, cmap="YlGnBu")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Depth (cm)")

    plt.gca().invert_yaxis()

    plt.xticks(rotation=45)

    def format_months(x, p):
        return pivot_table.columns[int(x)].strftime("%Y-%m")

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_months))
