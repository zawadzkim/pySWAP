"""Test for reading SWP files efficiently."""

from pathlib import Path

import pytest

from pyswap import load_swp
from pyswap.components.metadata import Metadata


@pytest.fixture
def swp_file_path():
    """Path to the test SWP file."""
    return Path(__file__).parent / "data" / "swap.swp"


@pytest.fixture
def minimal_metadata():
    """Create minimal metadata for fast loading."""
    return Metadata(
        author="Test",
        institution="Test Institution",
        email="test@example.com",
        project="Test Project",
        swap_ver="4.2.0",
    )


def test_load_swp_file(swp_file_path, minimal_metadata):
    """Test loading a SWP file - basic functionality."""
    # Load the model from the SWP file
    model = load_swp(swp_file_path, minimal_metadata)

    # Assert model is loaded
    assert model is not None

    # Check that key components exist
    assert model.generalsettings is not None
    assert model.meteorology is not None
    assert model.crop is not None
    assert model.soilprofile is not None


def test_load_swp_file_general_settings(swp_file_path, minimal_metadata):
    """Test that general settings are parsed correctly."""
    model = load_swp(swp_file_path, minimal_metadata)

    # Check general settings attributes
    assert model.metadata.project == "Test Project"  # Uses metadata passed in
    assert model.generalsettings.tstart is not None
    assert model.generalsettings.tend is not None


def test_load_swp_file_has_valid_structure(swp_file_path, minimal_metadata):
    """Test that the loaded model has a valid structure."""
    model = load_swp(swp_file_path, minimal_metadata)

    # Check that all major components are present
    components = [
        "generalsettings",
        "meteorology",
        "crop",
        "fixedirrigation",
        "soilmoisture",
        "surfaceflow",
        "evaporation",
        "soilprofile",
        "snowandfrost",
        "richardsettings",
        "lateraldrainage",
        "bottomboundary",
        "heatflow",
        "solutetransport",
    ]

    for component in components:
        assert hasattr(model, component), f"Missing component: {component}"
        assert getattr(model, component) is not None


def test_load_swp_file_can_serialize(swp_file_path, minimal_metadata):
    """Test that the loaded model can be serialized back to SWP format."""
    model = load_swp(swp_file_path, minimal_metadata)

    # Try to serialize the model
    swp_content = model.swp

    # Check that the serialization produces content
    assert swp_content is not None
    assert len(swp_content) > 0
    assert isinstance(swp_content, str)

    # Check that some key elements are in the output
    assert "PROJECT" in swp_content.upper()
    assert "TSTART" in swp_content.upper()


def test_load_swp_file_performance(swp_file_path, minimal_metadata):
    """Performance test for loading SWP files - measures execution time."""
    import time

    start = time.perf_counter()
    result = load_swp(swp_file_path, minimal_metadata)
    end = time.perf_counter()

    assert result is not None
    print(f"\nLoading SWP file took: {(end - start) * 1000:.2f} ms")
