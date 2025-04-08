import pandas as pd
import pytest

import pyswap.db.dutchsoilprofiles as dsp


def test_get_soilprofile_dutch_standards():
    # Make database object
    db = dsp.SoilProfilesDB()

    # Test with one soil profile id
    test = db.get_table_profiles(soilprofile_index=90110280)

    # Test with multiple soil profile ids
    test = db.get_table_profiles(soilprofile_index=[90110280, 1020])

    # Test with bofek cluster
    test = db.get_table_profiles(bofek_cluster=3001)

    # Test with multiple bofek clusters
    test = db.get_table_profiles(bofek_cluster=[3001, 3002])
    # print(test)

    # Test with soil profile code
    test = db.get_table_profiles(soilprofile_code="Hn21")
    print(test)

    # Test with multiple soil profile codes
    db.get_table_profiles(soilprofile_code=["Hn21", "pZg21"])

    # Test with all inputs:
    db.get_table_profiles(
        soilprofile_index=90110280, bofek_cluster=3001, soilprofile_code="Hn21"
    )

    # Test with dominant cluster profile
    test = db.get_table_profiles(
        bofek_cluster=3001,
        bofek_cluster_dominant=True,
    )
    # print(test)

    # Test with wrong input: soil profile id
    with pytest.raises(ValueError) as exc_info:
        db.get_table_profiles(soilprofile_index=9999999999)
    assert "Provide a valid soil profile number" in str(exc_info.value)

    # Test with wrong input: bofek cluster
    with pytest.raises(ValueError) as exc_info:
        db.get_table_profiles(bofek_cluster=9999999999)
    assert "Provide a valid soil profile number" in str(exc_info.value)

    # Test with wrong input: soil profile code
    with pytest.raises(ValueError) as exc_info:
        db.get_table_profiles(soilprofile_code="Hn9999999999")
    assert "Provide a valid soil profile number" in str(exc_info.value)


def test_soilprofile_hydrfunc():
    # Test if table values and headers are correct
    table_correct_sp = pd.read_csv("tests/test_bofeksoilprofile/bofek1001_sp.csv")
    table_correct_hf = pd.read_csv("tests/test_bofeksoilprofile/bofek1001_hf.csv")

    # Get database
    db = dsp.SoilProfilesDB()

    # Get soil profile
    sp = db.get_profile(bofek_cluster=1001)

    table_try_sp = sp.get_swapinput_profile(
        discretisation_depths=[50, 30, 60, 60, 100],
        discretisation_compheights=[1, 2, 5, 10, 20],
    )

    table_try_hf = sp.get_swapinput_hydraulic_params()

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
