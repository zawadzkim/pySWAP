import pandas as pd

import pyswap.components.soilwater as sw


def test_soilprofile_hydrfunc():
    # Test with soil profile id
    sw.soilprofile_from_Dutch_standards(soilprofile_ix=90110280)
    # Test with bofek cluster
    sw.soilprofile_from_Dutch_standards(bofek_cluster=3001)

    # Test if table values and headers are correct
    table_correct = pd.read_csv("tests/test_bofeksoilprofile/bofek1001.csv")
    table_correct_sp = table_correct.iloc[:, 0:5]
    table_correct_hf = table_correct.iloc[:, 5:]

    table_try_sp, table_try_hf = sw.soilprofile_from_Dutch_standards(bofek_cluster=1001)

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
    test_soilprofile_hydrfunc()
