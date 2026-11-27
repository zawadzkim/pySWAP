import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyswap.core.plot import evapotranspiration, water_content


def test_evapotranspiration_plots_two_lines():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    potential = pd.Series(np.linspace(1, 2, 10), index=dates)
    actual = potential * 0.8
    evapotranspiration(potential, actual)
    ax = plt.gcf().axes[0]
    assert [line.get_label() for line in ax.get_lines()] == ["Potential", "Actual"]
    assert plt.rcParams["font.size"] != 24  # style does not leak globally
    plt.close("all")


def test_water_content_heatmap():
    dates = pd.date_range("2020-01-01", periods=3, freq="MS")
    depths = [-5.0, -15.0, -25.0, -35.0]
    df = pd.DataFrame(
        [
            (z, d, 0.3 + 0.01 * i)
            for i, (z, d) in enumerate((z, d) for z in depths for d in dates)
        ],
        columns=["depth", "date", "wc"],
    )
    water_content(df, depth_col="depth", date_col="date", wcontent_col="wc")
    ax = plt.gcf().axes[0]
    assert ax.get_ylabel() == "Depth (cm)"
    assert [t.get_text() for t in ax.get_xticklabels()] == [
        "2020-01",
        "2020-02",
        "2020-03",
    ]
    assert [t.get_text() for t in ax.get_yticklabels()] == ["-35", "-25", "-15", "-5"]
    plt.close("all")
