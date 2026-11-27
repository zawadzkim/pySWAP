# mypy: disable-error-code="attr-defined"
# For some reason, the error was raised on the definition of month labels based
# on pivot table columns (which are dates). Error disabled for now. We will see
# if any bugs come up.

"""
Functions:
    water_content: Plot water content as heatmap.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from pyswap.core.plot._style import POSTER


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

    df_wcont = df[[depth_col, date_col, wcontent_col]]

    df_wcont.loc[:, date_col] = pd.to_datetime(df_wcont[date_col])
    df_wcont.loc[:, depth_col] = df_wcont[depth_col].astype(float)
    df_wcont.loc[:, wcontent_col] = df_wcont[wcontent_col].astype(float)

    pivot_table = df_wcont.pivot(columns=date_col, index=depth_col, values=wcontent_col)
    pivot_table = pivot_table.sort_index(axis=1)

    with plt.rc_context(POSTER):
        fig, ax = plt.subplots(figsize=(34, 8))
        # One cell per depth (rows) and date (columns); the first row of the
        # pivot table (smallest depth value) is drawn at the bottom.
        mesh = ax.pcolormesh(pivot_table.to_numpy(dtype=float), cmap="YlGnBu")
        fig.colorbar(mesh, ax=ax)

        n_depths, n_dates = pivot_table.shape
        ystep = max(1, n_depths // 20)
        xstep = max(1, n_dates // 20)
        ax.set_yticks(
            np.arange(0, n_depths, ystep) + 0.5,
            labels=[f"{d:g}" for d in pivot_table.index[::ystep]],
        )
        ax.set_xticks(
            np.arange(0, n_dates, xstep) + 0.5,
            labels=[d.strftime("%Y-%m") for d in pivot_table.columns[::xstep]],
            rotation=45,
        )

        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Depth (cm)")
