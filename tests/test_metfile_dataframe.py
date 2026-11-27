import pandas as pd

from pyswap import components
from pyswap.gis import Location

COLUMNS = [
    "STATION",
    "DD",
    "MM",
    "YYYY",
    "RAD",
    "TMIN",
    "TMAX",
    "HUM",
    "WIND",
    "RAIN",
    "ETREF",
    "WET",
]


def _user_dataframe():
    """Daily weather in a user's own DataFrame, columns in arbitrary order."""
    dates = pd.date_range("2020-01-01", periods=3, freq="D")
    return pd.DataFrame({
        "WET": [0.0, 0.5, 0.0],
        "STATION": "'my_station'",
        "DD": dates.day,
        "MM": dates.month,
        "YYYY": dates.year,
        "RAD": [2500.0, 2600.0, 2700.0],
        "TMIN": [-1.0, 0.0, 1.0],
        "TMAX": [4.0, 5.0, 6.0],
        "HUM": [0.6, 0.7, 0.8],
        "WIND": [2.0, 3.0, 4.0],
        "RAIN": [0.0, 5.0, 0.0],
        "ETREF": -99.9,
    })


def test_meteorology_from_a_user_dataframe(tmp_path):
    metfile = components.MetFile(metfil="My_Station.met", content=_user_dataframe())
    assert list(metfile.content.columns) == COLUMNS  # put in SWAP's order

    meteo = components.Meteorology(
        meteo_location=Location(lat=52.0, lon=21.0, alt=10.0),
        swetr=0,
        metfile=metfile,
        swdivide=1,
        swmetdetail=0,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
    )
    meteo.write_met(tmp_path)

    lines = (tmp_path / "my_station.met").read_text().splitlines()
    assert lines[0] == ",".join(COLUMNS)
    assert lines[1].startswith("'my_station',1,1,2020,2500.0")
    assert len(lines) == 4
