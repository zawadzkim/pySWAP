import pytest
from pandera.errors import SchemaError, SchemaErrors

from pyswap.components.tables import RDTB


def test_rdtb_accepts_rooting_depth_up_to_1000_cm():
    # SWAP reads RDTB with RD in [0, 1000] cm.
    table = RDTB.create({"DVS": [0.0, 2.0], "RD": [10.0, 1000.0]})
    assert table["RD"].max() == 1000.0


def test_rdtb_rejects_rooting_depth_above_1000_cm():
    with pytest.raises((SchemaError, SchemaErrors)):
        RDTB.create({"DVS": [0.0, 2.0], "RD": [10.0, 1001.0]})
