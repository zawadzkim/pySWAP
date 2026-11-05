from pathlib import Path

import pytest
from pydantic import ValidationError

import pyswap as psp


def test_misspelled_subsection_keyword_raises():
    settings = psp.components.crop.CropDevelopmentSettingsFixed(
        idev=1, lcc=366, kdif=0.6, kdir=0.75
    )
    with pytest.raises(ValidationError, match="crop_dev_settings"):
        psp.components.crop.CropFile(name="citrus", crop_dev_settings=settings)


def test_unnumbered_drainage_level_keyword_raises():
    with pytest.raises(ValidationError, match="drares"):
        psp.components.drainage.Flux(drares=100.0, swallo=3)


def test_unknown_general_settings_keyword_raises():
    with pytest.raises(ValidationError, match="tstrat"):
        psp.components.simsettings.GeneralSettings(tstrat="2020-01-01")


def test_load_swp_keeps_richards_settings_from_file():
    # load_swp passes the whole parsed file to every component's update(),
    # so keys belonging to other components must be skipped there; the
    # Richards settings must come from the file (SWKMEAN = 2, MAXBACKTR = 5),
    # not from the defaults (1 and 3).
    metadata = psp.components.metadata.Metadata(
        author="Test",
        institution="Test",
        email="test@example.com",
        project="Test",
        swap_ver="4.2.0",
    )
    model = psp.load_swp(Path(__file__).parent / "data" / "swap.swp", metadata)
    assert model.richardsettings.swkmean == 2
    assert model.richardsettings.maxbacktr == 5


def test_update_accepts_aliased_keys():
    # .crp files use TSUMEA/TSUMAM, the aliases of tsum1/tsum2.
    settings = psp.components.crop.CropDevelopmentSettingsFixed(idev=2)
    settings.update({"tsumea": 1050.0, "tsumam": 1000.0}, inplace=True)
    assert settings.tsum1 == 1050.0
    assert settings.tsum2 == 1000.0
