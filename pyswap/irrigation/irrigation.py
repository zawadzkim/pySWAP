""" "
Irrigation settings for the SWAP simuluation.

Classes:
    FixedIrrigation: Fixed irrigation settings.
    ScheduledIrrigation: Irrigation scheduling settings.
"""

from typing import Literal, Self

from pydantic import Field, model_validator

from ..core import YEARRANGE, DayMonth, PySWAPBaseModel, SerializableMixin, Table
from .irgfile import IrgFile


class FixedIrrigation(PySWAPBaseModel, SerializableMixin):
    """Fixed irrigation settings.

    !!! note
        This class is only used in the .swp file.

    Attributes:
        swirfix (Literal[0, 1]): Switch for fixed irrigation applications
        swirgfil (Literal[0, 1]): Switch for separate file with fixed irrigation applications
        table_irrigevents (Optional[Table]):
        irgfil (Optional[str]):
        irrigationdata (Optional[IrrigationFile]):
    """

    swirfix: Literal[0, 1]
    swirgfil: Literal[0, 1] | None = None
    table_irrigevents: Table | None = None
    irgfile: IrgFile | None = Field(default=None, repr=False)

    @model_validator(mode="after")
    def _validate_fixed_irrigation(self) -> Self:
        if self.swirfix == 1:
            if self.swirgfil:
                assert self.irgfile is not None, (
                    "irgfile is required when swirgfil is True"
                )
            else:
                assert self.table_irrigevents is not None, (
                    "irrigevents is required when swirgfil is False"
                )

        return self

    def write_irg(self, path) -> str:
        self.irgfile.save_file(
            string=self.irgfile.content,
            fname=self.irgfile.irgfil,
            path=path,
            extension="irg",
        )


class ScheduledIrrigation(PySWAPBaseModel, SerializableMixin):
    """Irrigation scheduling settings.

    !!! warning
        The docstring needs to be updated.

    !!! note
        This class is only used in the .crp file.

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

    schedule: Literal[0, 1]
    startirr: DayMonth | None = None
    endirr: DayMonth | None = None
    cirrs: float | None = Field(default=None, ge=0.0, le=100.0)
    isuas: Literal[0, 1] | None = None
    tcs: Literal[1, 2, 3, 4, 6, 7, 8] | None = None
    phfieldcapacity: float | None = Field(default=None, ge=-1000.0, le=0.0)
    irgthreshold: float | None = Field(default=None, ge=0.0, le=20.0)
    dcrit: float | None = Field(default=None, ge=-100.0, le=0.0)
    swcirrthres: Literal[0, 1] | None = None
    cirrthres: float | None = Field(default=None, ge=0.0, le=100.0)
    perirrsurp: float | None = Field(default=None, ge=0.0, le=100.0)
    tcsfix: Literal[0, 1] | None = None
    irgdayfix: int | None = Field(default=None, **YEARRANGE)
    dcs: Literal[0, 1] | None = None
    dcslim: Literal[0, 1] | None = None
    irgdepmin: float | None = Field(default=None, ge=0.0, le=100.0)
    irgdepmax: float | None = Field(default=None, ge=0.0, le=1.0e7)
    table_tc1tb: Table | None = None
    table_tc2tb: Table | None = None
    table_tc3tb: Table | None = None
    table_tc4tb: Table | None = None
    table_tc7tb: Table | None = None
    table_tc8tb: Table | None = None

    @model_validator(mode="after")
    def _validate_scheduled_irrigation(self) -> Self:
        if self.tcs == 1:
            self.dvs_tc1 = {"dvs_tc1": [0.0, 2.0], "Trel": [0.95, 0.95]}
        elif self.tcs == 2:
            self.dvs_tc2 = {"dvs_tc2": [0.0, 2.0], "RAW": [0.95, 0.95]}
        elif self.tcs == 3:
            self.dvs_tc3 = {"dvs_tc3": [0.0, 2.0], "TAW": [0.50, 0.50]}
        elif self.tcs == 4:
            self.dvs_tc4 = {"dvs_tc4": [0.0, 2.0], "DWA": [0.40, 0.40]}
        elif self.tcs == 5:
            self.dvs_tc5 = {"dvs_tc5": [0.0, 2.0], "Value_tc5": [-1000.0, -1000.0]}
        elif self.tcs == 6:
            assert self.irgthreshold is not None, (
                "irgthreshold is required when tcs is 6"
            )
            assert self.tcsfix is not None, "tcsfix is required when tcs is 6"
            if self.tcsfix:
                assert self.irgdayfix is not None, (
                    "irgdayfix is required when tcsfix is True"
                )

        return self
