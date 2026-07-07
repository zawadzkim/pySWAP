"""Unit tests for the WOFOST crop parameters database wrappers.

Covers pyswap.db.cropdb (WOFOSTCropDB, WOFOSTCropFile, CropVariety) by loading
a real crop file (potato) from the WOFOST_crop_parameters library.
"""

import pytest

from pyswap.db.cropdb import CropVariety, WOFOSTCropDB, WOFOSTCropFile
from pyswap.libs import crop_params


@pytest.fixture()
def potato():
    return WOFOSTCropDB().load_crop_file("potato")


@pytest.fixture()
def potato_variety(potato):
    return potato.get_variety("Potato_701")


# --- WOFOSTCropDB -----------------------------------------------------------


def test_default_libdir():
    assert WOFOSTCropDB().libdir == crop_params


def test_load_crop_file_returns_crop_file(potato):
    assert isinstance(potato, WOFOSTCropFile)


def test_load_crop_file_accepts_yaml_extension():
    with_ext = WOFOSTCropDB().load_crop_file("potato.yaml")
    assert with_ext.varieties == WOFOSTCropDB().load_crop_file("potato").varieties


def test_load_crop_file_missing_raises():
    with pytest.raises(FileNotFoundError):
        WOFOSTCropDB().load_crop_file("nonexistent_crop")


def test_croptypes_prints_available_crops(capsys):
    _ = WOFOSTCropDB().croptypes
    assert "potato" in capsys.readouterr().out


# --- WOFOSTCropFile ---------------------------------------------------------


def test_crop_file_metadata(potato):
    assert "Title" in potato.metadata


def test_crop_file_ecotypes(potato):
    assert "potato" in potato.ecotypes


def test_crop_file_varieties(potato):
    assert "Potato_701" in potato.varieties


def test_get_variety_returns_cropvariety(potato_variety):
    assert isinstance(potato_variety, CropVariety)


def test_get_variety_unknown_raises(potato):
    with pytest.raises(KeyError):
        potato.get_variety("does_not_exist")


# --- CropVariety ------------------------------------------------------------


def test_variety_parameters_lowercased_scalar(potato_variety):
    assert potato_variety.parameters["tbasem"] == 3.0


def test_variety_parameters_excludes_negative99(potato_variety):
    # Parameters with the -99.0 are dropped.
    assert all(value != -99.0 for value in potato_variety.parameters.values())


def test_variety_parameters_formats_tables(potato_variety):
    assert potato_variety.parameters["co2efftb"][:2] == [[40.0, 0.0], [360.0, 1.0]]


def test_variety_metadata(potato_variety):
    assert "Title" in potato_variety.metadata
