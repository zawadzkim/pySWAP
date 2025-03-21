import pandas as pd
import pytest

import pyswap.components.soilwater as sw


def test_get_soilprofile_dutch_standards():
    # Test with one soil profile id
    sw.get_soilprofiles_from_Dutch_standards(soilprofile_ix=90110280)

    # Test with multiple soil profile ids
    sw.get_soilprofiles_from_Dutch_standards(soilprofile_ix=[90110280, 1020])

    # Test with bofek cluster
    sw.get_soilprofiles_from_Dutch_standards(bofek_cluster=3001)

    # Test with multiple bofek clusters
    sw.get_soilprofiles_from_Dutch_standards(bofek_cluster=[3001, 3002])

    # Test with soil profile code
    sw.get_soilprofiles_from_Dutch_standards(soilprofile_code="Hn21")

    # Test with multiple soil profile codes
    sw.get_soilprofiles_from_Dutch_standards(soilprofile_code=["Hn21", "pZg21"])

    # Test with all inputs:
    sw.get_soilprofiles_from_Dutch_standards(
        soilprofile_ix=90110280, bofek_cluster=3001, soilprofile_code="Hn21"
    )

    # Test with wrong input: soil profile id
    with pytest.raises(ValueError) as exc_info:
        sw.get_soilprofiles_from_Dutch_standards(soilprofile_ix=9999999999)
    assert "Provide a valid soil profile number" in str(exc_info.value)

    # Test with wrong input: bofek cluster
    with pytest.raises(ValueError) as exc_info:
        sw.get_soilprofiles_from_Dutch_standards(bofek_cluster=9999999999)
    assert "Provide a valid soil profile number" in str(exc_info.value)

    # Test with wrong input: soil profile code
    with pytest.raises(ValueError) as exc_info:
        sw.get_soilprofiles_from_Dutch_standards(soilprofile_code="Hn9999999999")
    assert "Provide a valid soil profile number" in str(exc_info.value)


def test_soilprofile_hydrfunc():
    # Test if table values and headers are correct
    table_correct_sp = pd.read_csv("tests/test_bofeksoilprofile/bofek1001_sp.csv")
    table_correct_hf = pd.read_csv("tests/test_bofeksoilprofile/bofek1001_hf.csv")

    table_try_sp, table_try_hf = sw.input_soil_from_Dutch_standards(bofek_cluster=1001)

    pd.testing.assert_frame_equal(
        table_correct_sp,
        table_try_sp,
        check_dtype=False,
    )

    pd.testing.assert_frame_equal(
        table_correct_hf,
        table_try_hf,
        check_dtype=False,
    )


if __name__ == "__main__":
    test_get_soilprofile_dutch_standards()
    test_soilprofile_hydrfunc()
