"""Tests for the subsurface drip irrigation (SSDI) settings.

SSDI is a source term at depth in the Richards equation, available in SWAP
since 4.2.0 through the optional SWSSDI switch and a separate events file.
These tests cover the serialization only; the feature is exercised against
the SWAP executable in the regression cases.
"""

import pytest

from pyswap.components.irrigation import SSDIEVENTS, FixedIrrigation


@pytest.fixture
def ssdi_irrigation():
    events = SSDIEVENTS.create({
        "SSDI_DATE": ["2022-04-25", "2022-05-02"],
        "SSDI_RATE_F": [0.166, 0.266],
        "SSDI_AMOUNT_F": [3.98, 6.39],
    })
    return FixedIrrigation(swirfix=0, swssdi=1, ssdievents=events, ssdi_z=-100.0)


def test_ssdi_swp_section(ssdi_irrigation):
    """The .swp section carries the switch and file name, not the events."""
    section = ssdi_irrigation.model_string()

    assert "SWSSDI = 1" in section
    assert "SSDI_FILE = 'swap.ssdi'" in section
    assert "SSDI_DATE" not in section
    assert "SSDI_Z" not in section


def test_ssdi_file_content(ssdi_irrigation):
    """The SSDI file carries the schedule, the events table and the depth."""
    content = ssdi_irrigation.ssdi

    assert "SSDI_SCHEDULE = 0" in content
    assert "SSDI_DATE" in content
    assert "2022-04-25" in content
    assert "SSDI_Z = -100.00" in content


def test_ssdi_defaults():
    """Enabling the switch fills the file name and the schedule."""
    fi = FixedIrrigation(swirfix=0, swssdi=1, ssdi_z=-50.0)

    assert fi.ssdi_file == "swap.ssdi"
    assert fi.ssdi_schedule == 0


def test_ssdi_off_is_silent():
    """Without the switch, nothing SSDI-related leaks into the .swp section."""
    fi = FixedIrrigation(swirfix=0)

    assert "SSDI" not in fi.model_string()
    with pytest.raises(ValueError):
        fi.write_ssdi(".")


def test_ssdi_write(ssdi_irrigation, tmp_path):
    """write_ssdi creates the events file next to the model files."""
    ssdi_irrigation.write_ssdi(tmp_path)

    written = (tmp_path / "swap.ssdi").read_text()
    assert "SSDI_SCHEDULE = 0" in written
    assert "SSDI_Z = -100.00" in written
