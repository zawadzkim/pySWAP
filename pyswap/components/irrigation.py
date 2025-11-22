# mypy: disable-error-code="call-overload, misc, override"
# - override was raised on model_string, because the methods do not share the
#   same signature. This was not a proirity to fix.
"""Irrigation settings for the SWAP simuluation.

Classes:
    IrgFile: The irrigation file.
    FixedIrrigation: Fixed irrigation settings.
    ScheduledIrrigation: Irrigation scheduling settings.

Functions:
    irg_from_csv: Load the irrigation file from a CSV file.
"""

from pathlib import Path as _Path
from typing import Literal as _Literal

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import IRRIGEVENTS
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import FNAME_IN as _FNAME_IN
from pyswap.core.fields import (
    DayMonth as _DayMonth,
    String as _String,
    Table as _Table,
)
from pyswap.core.valueranges import YEARRANGE as _YEARRANGE
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = ["IRRIGEVENTS", "FixedIrrigation", "ScheduledIrrigation"]


class FixedIrrigation(
    _PySWAPBaseModel, _SerializableMixin, _FileMixin, _YAMLValidatorMixin
):
    """Fixed irrigation settings in the .swp file.

    Attributes:
        swirfix (Literal[0, 1]): Switch for fixed irrigation applications
        swirgfil (Literal[0, 1]): Switch for separate file with fixed irrigation applications
        irrigevents (Optional[Table]):
        irgfil (Optional[str]):
    """

    _extension = _PrivateAttr(default="irg")

    swirfix: _Literal[0, 1] | None = None
    swirgfil: _Literal[0, 1] | None = None
    irgfil: _String = _Field(default=_FNAME_IN, frozen=True)
    irrigevents: _Table | None = None

    def model_string(self, **kwargs) -> str:
        """Override the model_string to handle optional file generation.

        Return the full section if swirgfil is set to 1, otherwise, irrigevents
        is excluded from the string and saved in a separate .irg file.
        """
        if self.swirgfil == 1:
            return super().model_string(exclude={"irrigevents"}, **kwargs)
        else:
            return super().model_string()

    @property
    def irg(self):
        return super().model_string(include={"irrigevents"})

    def write_irg(self, path: _Path):
        """Write irrigation data to .irg file.

        This method is only available when the swirgfil attribute is set to 1.

        Parameters:
            path (Path): Path to the directory where the .irg file will be
                saved.
        """
        if self.swirgfil != 1:
            msg = "Irrigation data are not set to be written to a .irg file."
            raise ValueError(msg)

        self.save_file(string=self.irg, fname=self.irgfil, path=path)


class ScheduledIrrigation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Irrigation scheduling settings in the .crp file.

    Attributes:
        schedule (Literal[0, 1]): Switch for application irrigation scheduling
        startirr (str): Specify day and month at which irrigation scheduling starts
        endirr (str): Specify day and month at which irrigation scheduling stops
        cirrs (float): Solute concentration of irrigation water
        isuas (int): Switch for type of irrigation method

            * 0 - Sprinkler irrigation
            * 1 - Surface irrigation

        tcs (int): Choose one of the following timing criteria options

            * 1 - Ratio actual/potential transpiration
            * 2 - Depletion of Readily Available Water
            * 3 - Depletion of Totally Available Water
            * 4 - Depletion of absolute Water Amount
            * 6 - Fixed weekly irrigation
            * 7 - Pressure head
            * 8 - Moisture content

        phFieldCapacity (float): Soil water pressure head at field capacity
        irgthreshold (Optional[float]): Threshold value for weekly irrigation
        dcrit (Optional[float]): Depth of the sensor
        swcirrthres (Optional[bool]): Switch for over-irrigation
        cirrthres (Optional[float]): Threshold salinity concentration above which over-irrigation occur
        perirrsurp (Optional[float]): Over-irrigation of the usually scheduled irrigation depth
        tcsfix (Optional[int]): Switch for minimum time interval between irrigation applications
        irgdayfix (Optional[int]): Minimum number of days between irrigation applications
        phormc (Optional[int]): Switch for the use of pressure head or water content

            * 0 - Pressure head
            * 1 - Water content

        dvs_tc1 (Optional[Table]):
        dvs_tc2 (Optional[Table]):
        dvs_tc3 (Optional[Table]):
        dvs_tc4 (Optional[Table]):
        dvs_tc5 (Optional[Table]):
    """

    schedule: _Literal[0, 1] | None = None
    startirr: _DayMonth | None = None
    endirr: _DayMonth | None = None
    cirrs: float | None = _Field(default=None, ge=0.0, le=100.0)
    isuas: _Literal[0, 1] | None = None
    tcs: _Literal[1, 2, 3, 4, 6, 7, 8] | None = None

    phfieldcapacity: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    irgthreshold: float | None = _Field(default=None, ge=0.0, le=20.0)
    dcrit: float | None = _Field(default=None, ge=-100.0, le=0.0)
    swcirrthres: _Literal[0, 1] | None = None
    cirrthres: float | None = _Field(default=None, ge=0.0, le=100.0)
    perirrsurp: float | None = _Field(default=None, ge=0.0, le=100.0)
    tcsfix: _Literal[0, 1] | None = None
    irgdayfix: int | None = _Field(default=None, **_YEARRANGE)
    dcs: _Literal[0, 1] | None = None
    dcslim: _Literal[0, 1] | None = None
    irgdepmin: float | None = _Field(default=None, ge=0.0, le=100.0)
    irgdepmax: float | None = _Field(default=None, ge=0.0, le=1.0e7)
    tc1tb: _Table | None = None
    tc2tb: _Table | None = None
    tc3tb: _Table | None = None
    tc4tb: _Table | None = None
    tc7tb: _Table | None = None
    tc8tb: _Table | None = None
    dc1tb: _Table | None = None
    dc2tb: _Table | None = None
