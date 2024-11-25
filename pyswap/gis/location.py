from decimal import Decimal

from pydantic import Field, field_validator
from pyproj import CRS, Transformer
from shapely import Point

from pyswap.core.basemodel import PySWAPBaseModel


class Location(PySWAPBaseModel):
    """Location of the PySWAP model.

    Arguments:
        lon (Decimal): point longitude.
        lat (Decimal): point latitude.
        lat (Decimal): point elevation in meters.
        crs (string): Coordinate Reference System of the input coordinates.
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
            return v
        except:
            raise ValueError(f"Invalid CRS: {v}")

    def to_crs(self, target_crs: str) -> "Location":
        try:
            target_crs_obj = CRS.from_user_input(target_crs)
        except:
            raise ValueError(f"Invalid target CRS: {target_crs}")

        transformer = Transformer.from_crs(self.crs, target_crs, always_xy=True)

        new_lon, new_lat, new_alt = transformer.transform(self.lon, self.lat, self.alt)

        return self.model_copy(
            update={"lon": new_lon, "lat": new_lat, "alt": new_alt, "crs": target_crs}
        )
