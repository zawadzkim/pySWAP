import re
from pathlib import Path

import pytest
from pydantic import ValidationError

from pyswap.components.crop import (
    CFTB,
    GCTB,
    RDCTB,
    RDTB,
    CropDevelopmentSettingsFixed,
    CropFile,
)
from pyswap.utils.loaders import load_crp

MAIZE_CRP = Path(__file__).parents[1] / "pyswap/testcase/data/1-hupselbrook/maizes.crp"

FIXED = {
    "idev": 1,
    "lcc": 168,
    "swcf": 1,
    "cftb": CFTB.create({"DVS": [0.0, 2.0], "CF": [0.8, 1.2]}),
    "kdif": 0.6,
    "kdir": 0.75,
    "swgc": 1,
    "gctb": GCTB.create({"DVS": [0.0, 2.0], "LAI": [0.05, 4.0]}),
    "swrd": 1,
    "rdtb": RDTB.create({"DVS": [0.0, 2.0], "RD": [10.0, 50.0]}),
    "rdctb": RDCTB.create({"RRD": [0.0, 1.0], "RDENS": [1.0, 0.0]}),
}


def crp(**settings):
    cropdev = CropDevelopmentSettingsFixed(**settings)
    return CropFile(name="test", cropdev_settings=cropdev).crp


def test_complete_fixed_crop_settings_pass():
    assert "IDEV = 1" in crp(**FIXED)


@pytest.mark.parametrize("missing", ["idev", "swcf", "kdif", "kdir", "swgc", "rdctb"])
def test_fixed_crop_requires_parameters_swap_always_reads(missing):
    settings = {k: v for k, v in FIXED.items() if k != missing}
    with pytest.raises(ValueError, match=missing):
        crp(**settings)


def test_fixed_duration_requires_lcc():
    settings = {k: v for k, v in FIXED.items() if k != "lcc"}
    with pytest.raises(ValueError, match="lcc"):
        crp(**settings)


def test_variable_duration_requires_temperature_sums():
    settings = {k: v for k, v in FIXED.items() if k != "lcc"} | {"idev": 2}
    with pytest.raises(ValueError, match="tsum1, tsum2, tbase"):
        crp(**settings)


def test_swgc_requires_gctb():
    settings = {k: v for k, v in FIXED.items() if k != "gctb"}
    with pytest.raises(ValueError, match="gctb"):
        crp(**settings)


def test_soil_cover_fraction_table_for_swgc_2():
    gctb = GCTB.create({"DVS": [0.0, 2.0], "SCF": [0.05, 0.9]})
    assert "GCTB" in crp(**FIXED | {"swgc": 2, "gctb": gctb})


@pytest.mark.parametrize(("swgc", "column"), [(1, "SCF"), (2, "LAI")])
def test_gctb_column_must_match_swgc(swgc, column):
    gctb = GCTB.create({"DVS": [0.0, 2.0], column: [0.05, 0.9]})
    with pytest.raises(ValidationError, match="gctb"):
        CropDevelopmentSettingsFixed(swgc=swgc, gctb=gctb)


def test_load_crp_reads_soil_cover_fraction(tmp_path):
    text = MAIZE_CRP.read_text()
    text = text.replace("SWGC = 1", "SWGC = 2")
    text = re.sub(
        r"GCTB =\n.*?\* End of table",
        "GCTB =\n0.0 0.05\n2.0 0.9\n* End of table",
        text,
        flags=re.DOTALL,
    )
    path = tmp_path / "maizes.crp"
    path.write_text(text)

    cropdev = load_crp(path, "fixed", "maize").cropdev_settings
    assert cropdev.swgc == 2
    assert list(cropdev.gctb.columns) == ["DVS", "SCF"]
