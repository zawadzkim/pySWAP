import pytest
from pyproj import Transformer
from shapely.geometry import Point
from pyswap import ModelLocation


def test_ModelLocation_initialization():
    """Test that ModelLocation initializes correctly with valid input."""
    loc = ModelLocation(
        lat=40.7128,
        lon=-74.0060,
        alt=10.0,
        crs="EPSG:4326"
    )

    assert float(loc.lat) == pytest.approx(40.7128)
    assert float(loc.lon) == pytest.approx(-74.0060)
    assert float(loc.alt) == pytest.approx(10.0)
    assert loc.crs == "EPSG:4326"
    assert isinstance(loc.point(), Point)


def test_ModelLocation_invalid_crs():
    """Test that ModelLocation raises an error with an invalid CRS."""
    with pytest.raises(ValueError, match="Invalid CRS"):
        ModelLocation(
            lon=-74.0060,
            lat=40.7128,
            alt=10.0,
            crs="INVALID_CRS"
        )


def test_ModelLocation_to_crs():
    """Test that the ModelLocation correctly transforms to a new CRS."""
    loc = ModelLocation(
        lon=-74.0060,
        lat=40.7128,
        alt=10.0,
        crs="EPSG:4326"
    )

    loc_utm = loc.to_crs("EPSG:32618")  # UTM Zone 18N

    # Validate that the CRS has changed
    assert loc_utm.crs == "EPSG:32618"

    # Validate that the coordinates have transformed
    transformer = Transformer.from_crs(
        "EPSG:4326", "EPSG:32618", always_xy=True)
    expected_lon, expected_lat, expected_alt = transformer.transform(
        -74.0060, 40.7128, 10.0)

    assert float(loc_utm.lon) == pytest.approx(expected_lon)
    assert float(loc_utm.lat) == pytest.approx(expected_lat)
    assert float(loc_utm.alt) == pytest.approx(expected_alt)


def test_ModelLocation_point_method():
    """Test that the point method returns a correct Shapely Point object."""
    loc = ModelLocation(
        lon=-74.0060,
        lat=40.7128,
        alt=10.0,
        crs="EPSG:4326"
    )

    point = loc.point()
    assert isinstance(point, Point)
    assert point.x == pytest.approx(-74.0060)
    assert point.y == pytest.approx(40.7128)
    assert point.z == pytest.approx(10.0)
