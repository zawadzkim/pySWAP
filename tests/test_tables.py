import pytest
from pandera.errors import SchemaError, SchemaErrors

from pyswap.components.tables import GCTB, RDTB


def test_rdtb_accepts_rooting_depth_up_to_1000_cm():
    # SWAP reads RDTB with RD in [0, 1000] cm.
    table = RDTB.create({"DVS": [0.0, 2.0], "RD": [10.0, 1000.0]})
    assert table["RD"].max() == 1000.0


def test_rdtb_rejects_rooting_depth_above_1000_cm():
    with pytest.raises((SchemaError, SchemaErrors)):
        RDTB.create({"DVS": [0.0, 2.0], "RD": [10.0, 1001.0]})


@pytest.mark.parametrize(
    ("column", "values"), [("LAI", [0.05, 12.0]), ("SCF", [0.05, 1.0])]
)
def test_gctb_accepts_lai_or_scf(column, values):
    table = GCTB.create({"DVS": [0.0, 2.0], column: values})
    assert list(table.columns) == ["DVS", column]


@pytest.mark.parametrize(
    "data",
    [
        {"DVS": [0.0, 2.0], "SCF": [0.05, 1.5]},
        {"DVS": [0.0, 2.0], "LAI": [0.05, 13.0]},
        {"DVS": [0.0, 2.0], "LAI": [0.05, 4.0], "SCF": [0.05, 1.0]},
        {"DVS": [0.0, 2.0]},
    ],
    ids=["scf-above-1", "lai-above-12", "both", "neither"],
)
def test_gctb_rejects_invalid_tables(data):
    with pytest.raises((SchemaError, SchemaErrors)):
        GCTB.create(data)
