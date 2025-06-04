# mypy: disable-error-code="no-any-unimported"
# This error was due to lack of stubs for shapely.
"""Location class and related functionality.

Classes:
    Location: A generic class representing a location.
"""

from decimal import Decimal

from pydantic import Field, field_validator
from pyproj import CRS, Transformer
from shapely.geometry import Point

from pyswap.core.basemodel import PySWAPBaseModel


class Location(PySWAPBaseModel):
    """A generic class representing a location.

    This class can represent any location used in the package, e.g., weather
    station, model soil column, etc.).

    Attributes:
        lon (Decimal): point longitude.
        lat (Decimal): point latitude.
        lat (Decimal): point elevation in meters.
        crs (string): Coordinate Reference System of the input coordinates.

    Properties:
        point: Return a Shapely Point object.

    Methods:
        to_crs: Transform the location to a new Coordinate Reference System.
    """

    lon: Decimal
    lat: Decimal
    alt: Decimal
    crs: str = Field(default="EPSG:4326", exclude=True)

    @property
    def point(self) -> Point:
        """Return a Shapely Point object"""
        return Point(self.lon, self.lat, self.alt)

    @field_validator("crs")
    def validate_crs(cls, v):
        try:
            CRS.from_user_input(v)
        except Exception:
            msg = f"Invalid CRS: {v}"
            raise ValueError(msg) from None
        else:
            return v

    def to_crs(self, target_crs: str) -> "Location":
        """Transform the location to a new Coordinate Reference System.

        Arguments:
            target_crs (str): The target CRS.

        Returns:
            Location: A new Location object with the transformed coordinates.
        """

        CRS.from_user_input(target_crs)

        transformer = Transformer.from_crs(self.crs, target_crs, always_xy=True)

        new_lon, new_lat, new_alt = transformer.transform(self.lon, self.lat, self.alt)

        return self.model_copy(
            update={"lon": new_lon, "lat": new_lat, "alt": new_alt, "crs": target_crs},
            deep=True,
        )
