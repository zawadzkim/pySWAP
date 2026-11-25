# mypy: disable-error-code="no-any-unimported"
# This error was due to lack of stubs for shapely.
"""Location class and related functionality.

Classes:
    Location: A generic class representing a location.

A Location is plain coordinates (lon, lat, alt) and works with the core
install. Coordinate reference system support (validating a CRS other than
the default, `to_crs`) and the Shapely `point` need the optional `gis` extra:
`pip install "pyswap[gis]"` (pyproj and shapely).
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import Field, field_validator

from pyswap.core.basemodel import PySWAPBaseModel

if TYPE_CHECKING:
    from shapely.geometry import Point

_DEFAULT_CRS = "EPSG:4326"


def _gis_import_error(feature: str) -> ImportError:
    msg = (
        f"{feature} needs the optional GIS dependencies (pyproj, shapely). "
        'Install them with: pip install "pyswap[gis]"'
    )
    return ImportError(msg)


class Location(PySWAPBaseModel):
    """A generic class representing a location.

    This class can represent any location used in the package, e.g., weather
    station, model soil column, etc.). Plain coordinates in the default CRS
    (EPSG:4326, longitude/latitude) need no extra dependencies.

    Attributes:
        lon (Decimal): point longitude.
        lat (Decimal): point latitude.
        alt (Decimal): point elevation in meters.
        crs (string): Coordinate Reference System of the input coordinates.
            Any CRS other than the default is validated with pyproj and needs
            the `gis` extra.

    Properties:
        point: Return a Shapely Point object (needs the `gis` extra).

    Methods:
        to_crs: Transform the location to a new Coordinate Reference System
            (needs the `gis` extra).
    """

    lon: Decimal
    lat: Decimal
    alt: Decimal
    crs: str = Field(default=_DEFAULT_CRS, exclude=True)

    @property
    def point(self) -> Point:
        """Return a Shapely Point object"""
        try:
            from shapely.geometry import Point
        except ImportError as e:
            raise _gis_import_error("Location.point") from e
        return Point(self.lon, self.lat, self.alt)

    @field_validator("crs")
    @classmethod
    def validate_crs(cls, v):
        if v == _DEFAULT_CRS:
            return v
        try:
            from pyproj import CRS
        except ImportError as e:
            feature = f"Using the CRS {v!r}"
            raise _gis_import_error(feature) from e
        try:
            CRS.from_user_input(v)
        except Exception:
            msg = f"Invalid CRS: {v}"
            raise ValueError(msg) from None
        else:
            return v

    def to_crs(self, target_crs: str) -> Location:
        """Transform the location to a new Coordinate Reference System.

        Arguments:
            target_crs (str): The target CRS.

        Returns:
            Location: A new Location object with the transformed coordinates.
        """
        try:
            from pyproj import CRS, Transformer
        except ImportError as e:
            raise _gis_import_error("Location.to_crs") from e

        CRS.from_user_input(target_crs)

        transformer = Transformer.from_crs(self.crs, target_crs, always_xy=True)

        new_lon, new_lat, new_alt = transformer.transform(self.lon, self.lat, self.alt)

        return self.model_copy(
            update={"lon": new_lon, "lat": new_lat, "alt": new_alt, "crs": target_crs},
            deep=True,
        )
