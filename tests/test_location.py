from decimal import Decimal

import pytest
from pydantic import ValidationError

from pyswap.components.meteorology import Meteorology
from pyswap.gis import Location


def test_meteorology_other_fields():
    location = Location(lat=Decimal("52.0"), lon=Decimal("21.0"), alt=Decimal("10.0"))

    meteo = Meteorology(
        meteo_location=location,
        swetr=0,
        swdivide=1,
        swmetdetail=0,
        altw=Decimal("10.0"),
        angstroma=Decimal("0.25"),
        angstromb=Decimal("0.5"),
    )

    assert meteo.lat == Decimal("52.0")
    assert meteo.alt == Decimal("10.0")
    assert meteo.swetr == 0
    assert meteo.swdivide == 1
    assert meteo.swmetdetail == 0
    assert meteo.altw == Decimal("10.00")
    assert meteo.angstroma == Decimal("0.25")
    assert meteo.angstromb == Decimal("0.50")


def test_wrong_crs():
    with pytest.raises(ValidationError) as exc_info:
        Location(lat=52.0, lon=21.0, alt=10.0, crs="INVALID_CRS")

    assert "Invalid CRS" in str(exc_info.value)


def test_crs_transformation_to_belgian_lambert():
    location = Location(lon=4.3528, lat=50.8466, alt=20.0)

    belgian_lambert = location.to_crs("EPSG:31370")

    assert belgian_lambert.crs == "EPSG:31370"

    assert pytest.approx(float(belgian_lambert.lon), abs=1) == 148876.55
    assert pytest.approx(float(belgian_lambert.lat), abs=1) == 170688.55

    assert belgian_lambert.alt == location.alt

    assert location.crs == "EPSG:4326"
    assert float(location.lon) == 4.3528
    assert float(location.lat) == 50.8466
