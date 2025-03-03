import pandas as pd
import pytest
from pandera.errors import SchemaError

import pyswap as psp
import pyswap.components.meteorology as meteo
import pyswap.testcase as testcase


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
        start="20200103",
        end="20200103",
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
        rtol=1e-2,
    )


def test_hupsel_with_knmi_input():
    model = testcase.get("hupselbrook")

    metfile = psp.components.meteorology.metfile_from_knmi(
        metfil="knmitest.met", stations="260", start="2002-01-01", end="2004-12-31"
    )

    meteo = psp.components.meteorology.Meteorology(
        metfile=metfile,
        lat=52.0,
        alt=2,  # m
        swetr=0,  # Penman-Monteith
        angstroma=0.25,  # TODO
        angstromb=0.50,  # TODO
        swmetdetail=0,  # daily data
        swdivide=1,  # divide E and T using PM
        swrain=0,  # Use only daily rainfall amounts
        swetsine=0,  # Distribute Tp and Ep over the day using a sine wave
        altw=2.0,  # wind, m
    )

    model.meteorology = meteo

    model.run("./", silence_warnings=True)
