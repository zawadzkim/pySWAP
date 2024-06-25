""""
Irrigation settings for the SWAP simuluation.

Classes:
    FixedIrrigation: Holds the settings for fixed irrigation.
    ScheduledIrrigation: Holds the settings for scheduled irrigation.
    Irrigation: Holds the irrigation settings of the simulation.
"""
from ..core import PySWAPBaseModel, Table, YEARRANGE, DayMonth
from typing import Optional, Literal, Any
from typing_extensions import Self
from pydantic import model_validator, Field
from .irgfile import IrgFile


class FixedIrrigation(PySWAPBaseModel):
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
    swirgfil: Optional[Literal[0, 1]] = None
    table_irrigevents: Optional[Table] = None
    irgfile: Optional[IrgFile] = Field(
        default=None, repr=False)

    @model_validator(mode='after')
    def _validate_fixed_irrigation(self) -> Self:
        if self.swirfix == 1:
            if self.swirgfil:
                assert self.irgfile is not None, "irgfile is required when swirgfil is True"
            else:
                assert self.table_irrigevents is not None, "irrigevents is required when swirgfil is False"

        return self


class ScheduledIrrigation(PySWAPBaseModel):
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
    startirr: Optional[DayMonth] = None
    endirr: Optional[DayMonth] = None
    cirrs: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    isuas: Optional[Literal[0, 1]] = None
    tcs: Optional[Literal[1, 2, 3, 4, 6, 7, 8]] = None
    phfieldcapacity: Optional[float] = Field(default=None, ge=-1000.0, le=0.0)
    irgthreshold: Optional[float] = Field(default=None, ge=0.0, le=20.0)
    dcrit: Optional[float] = Field(default=None, ge=-100.0, le=0.0)
    swcirrthres: Optional[Literal[0, 1]] = None
    cirrthres: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    perirrsurp: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    tcsfix: Optional[Literal[0, 1]] = None
    irgdayfix: Optional[int] = Field(default=None, **YEARRANGE)
    dcs: Optional[Literal[0, 1]] = None
    dcslim: Optional[Literal[0, 1]] = None
    irgdepmin: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    irgdepmax: Optional[float] = Field(default=None, ge=0.0, le=1.0e7)
    table_tc1tb: Optional[Table] = None
    table_tc2tb: Optional[Table] = None
    table_tc3tb: Optional[Table] = None
    table_tc4tb: Optional[Table] = None
    table_tc7tb: Optional[Table] = None
    table_tc8tb: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_scheduled_irrigation(self) -> Self:

        if self.tcs == 1:
            self.dvs_tc1 = {'dvs_tc1': [0.0, 2.0],
                            'Trel': [0.95, 0.95]}
        elif self.tcs == 2:
            self.dvs_tc2 = {'dvs_tc2': [0.0, 2.0],
                            'RAW': [0.95, 0.95]}
        elif self.tcs == 3:
            self.dvs_tc3 = {'dvs_tc3': [0.0, 2.0],
                            'TAW': [0.50, 0.50]}
        elif self.tcs == 4:
            self.dvs_tc4 = {'dvs_tc4': [0.0, 2.0],
                            'DWA': [0.40, 0.40]}
        elif self.tcs == 5:
            self.dvs_tc5 = {'dvs_tc5': [0.0, 2.0],
                            'Value_tc5': [-1000.0, -1000.0]}
        elif self.tcs == 6:
            assert self.irgthreshold is not None, "irgthreshold is required when tcs is 6"
            assert self.tcsfix is not None, "tcsfix is required when tcs is 6"
            if self.tcsfix:
                assert self.irgdayfix is not None, "irgdayfix is required when tcsfix is True"

        return self
