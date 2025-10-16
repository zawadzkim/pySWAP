import pandas as pd

import pyswap.db.co2concentration as co2


def test_get_filtered_co2file():
    co2_db = co2.CO2concentration()

    # Test with a valid period
    period = ["2000-01-01", "2020-12-31"]
    data = co2_db.get_filtered_co2file(period)

    # Load expected data
    expected_data = pd.read_csv(
        "tests/test_co2concentration/Atmospheric.co2",
        delimiter=" ",
        index_col=0,
    )

    # Check if the data is equal
    pd.testing.assert_frame_equal(
        expected_data,
        data,
        check_dtype=False,
    )


def test_write_co2():
    co2_db = co2.CO2concentration()

    # Test with a valid period
    period = ["2000-01-01", "2020-12-31"]
    directory = "tests/test_co2concentration/write/"
    co2_db.write_co2(directory, period)


if __name__ == "__main__":
    test_get_filtered_co2file()
    # test_write_co2()
