import pandas as pd
import pytest
from pandera.errors import SchemaError

import pyswap.components.meteorology as meteo


def test_metfile_from_csv():
    # Test correct csv file
    table_test = meteo.metfile_from_csv(
        metfil="test_meteo_1.csv", csv_path="tests/test_meteo/test_meteo_1.csv"
    )
    # expected output
    table_exp = pd.read_csv("tests/test_meteo/test_meteo_1.csv")
    table_exp = table_exp.rename(
        {col: col.upper() for col in table_exp.columns}, axis=1
    )
    # Compare
    pd.testing.assert_frame_equal(
        table_test.content,
        table_exp,
        check_dtype=False,
    )

    # Test csv file with missing column
    with pytest.raises(SchemaError) as exc_info:
        table_test = meteo.metfile_from_csv(
            metfil="test_meteo_2.csv", csv_path="tests/test_meteo/test_meteo_2.csv"
        )
    assert "not in dataframe. Columns in dataframe:" in str(exc_info.value)

    # Test csv file with string value instead of float
    with pytest.raises(SchemaError) as exc_info:
        table_test = meteo.metfile_from_csv(
            metfil="test_meteo_3.csv", csv_path="tests/test_meteo/test_meteo_3.csv"
        )
    assert "Error while coercing" in str(exc_info.value)

    # Test csv file with float value instead of string
    with pytest.raises(SchemaError) as exc_info:
        table_test = meteo.metfile_from_csv(
            metfil="test_meteo_4.csv", csv_path="tests/test_meteo/test_meteo_4.csv"
        )
    assert "Error while coercing" in str(exc_info.value)

    # Test if station field starts with '
    table_test = meteo.metfile_from_csv(
        metfil="test_meteo_5.csv", csv_path="tests/test_meteo/test_meteo_5.csv"
    )
    assert table_test.content["STATION"].iloc[0].startswith("'")


def test_metfile_from_knmi():
    # Test default variables
    table_test = meteo.metfile_from_knmi(
        metfil="test_knmi",
        stations="260",
        start="20200101",
        end="20200101",
        variables=None,
    ).content
    # expected output
    table_exp = pd.read_csv("tests/test_meteo/test_knmi.csv")
    table_exp["STATION"] = table_exp["STATION"].astype(str)
    table_exp.loc[:, "STATION"] = table_exp.STATION.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x
    )
    table_exp["DD"] = table_exp["DD"].astype(str)
    table_exp["MM"] = table_exp["MM"].astype(str)
    table_exp["YYYY"] = table_exp["YYYY"].astype(str)
    # Compare
    pd.testing.assert_frame_equal(
        table_test,
        table_exp,
        check_dtype=False,
    )

    # Test with a missing variable
    with pytest.raises(SchemaError) as exc_info:
        table_test = meteo.metfile_from_knmi(
            metfil="test_knmi",
            stations="260",
            start="20200101",
            end="20200102",
            variables=["TN", "TX", "UG", "DR", "FG", "RH", "EV24"],
        )
    assert "not in dataframe. Columns in dataframe:" in str(exc_info.value)
