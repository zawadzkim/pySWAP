"""Irrigation settings for the SWAP simuluation.

Classes:
    IrgFile: The irrigation file.
    FixedIrrigation: Fixed irrigation settings.
    ScheduledIrrigation: Irrigation scheduling settings.

Functions:
    irg_from_csv: Load the irrigation file from a CSV file.
"""

from typing import Literal as _Literal

from pandas import DataFrame as _DataFrame, read_csv as _read_csv
from pydantic import Field as _Field

from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import DayMonth as _DayMonth, String as _String, Table as _Table
from pyswap.core.mixins import FileMixin as _FileMixin, SerializableMixin as _SerializableMixin, YAMLValidatorMixin as _YAMLValidatorMixin
from pyswap.core.valueranges import YEARRANGE as _YEARRANGE

__all__ = ["IrgFile", "FixedIrrigation", "ScheduledIrrigation"]


class IrgFile(_PySWAPBaseModel, _FileMixin):
    """The irrigation file.

    Attributes:
        irgfil (str): the name of the irgfile without .irg extension.
        content (DataFrame): The content of the irrigation file.
    """

    irgfil: _String
    content: _DataFrame = _Field(exclude=True)


class FixedIrrigation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Fixed irrigation settings in the .swp file.

    Attributes:
        swirfix (Literal[0, 1]): Switch for fixed irrigation applications
        swirgfil (Literal[0, 1]): Switch for separate file with fixed irrigation applications
        table_irrigevents (Optional[Table]):
        irgfil (Optional[str]):
        irrigationdata (Optional[IrrigationFile]):
    """

    swirfix: _Literal[0, 1] | None = None
    swirgfil: _Literal[0, 1] | None = None
    irrigevents: _Table | None = None
    irgfile: IrgFile | None = _Field(default=None, repr=False)

    def write_irg(self, path) -> str:
        self.irgfile.save_file(
            string=self.irgfile.content,
            fname=self.irgfile.irgfil,
            path=path,
            extension="irg",
        )


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


def irg_from_csv(irgfil: str, path: str) -> IrgFile:
    """Load the irrigation file from a CSV file.

    Parameters:
        irgfil (str): the name of the irgfile without .irg extension.
        path (str): The path to the CSV file.

    Returns:
        IrgFile: The irrigation file.
    """
    return IrgFile(content=_read_csv(path), irgfil=irgfil)
