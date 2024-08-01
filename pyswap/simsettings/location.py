from ..core import PySWAPBaseModel
from shapely import Point


class Location(PySWAPBaseModel):
    point: Point

    @property
    def x(self):
        pass

    @property
    def y(self):
        pass

    @property
    def z(self):
        pass
