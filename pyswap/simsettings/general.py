import platform
from datetime import date
from typing import Literal, Self, ClassVar, List

from pydantic import Field, model_validator, ConfigDict, field_validator

from ..core import (
    UNITRANGE,
    YEARRANGE,
    DateList,
    DayMonth,
    FloatList,
    PySWAPBaseModel,
    SerializableMixin,
    String,
    StringList,
)

IS_WINDOWS = platform.system() == "Windows"
BASE_PATH = ".\\" if IS_WINDOWS else "./"


class GeneralSettings(PySWAPBaseModel, SerializableMixin):
    """General settings of the simulation.

    !!! todo
        * remove the individual file extension switches and replace with a
        list of extensions. Make the class automatically generate the switches
        based on the list of extensions.

    Attributes:
        pathwork (str): Path to the working directory. Immutable attribute.
        pathatm (str): Path to folder with weather files. Immutable attribute.
        pathcrop (str): Path to folder with crop files. Immutable attribute.
        pathdrain (str): Path to folder with drainage files. Immutable attribute.
        swscre (Literal[0, 1, 3]): Switch, display progression of simulation
            run to screen
        swerror (Literal[0, 1]): Switch for printing errors to screen
        tstart (d): Start date of simulation run, give day-month-year
        tend (d): End date of simulation run, give day-month-year
        nprintday (int): Number of output times during a day
        swmonth (Literal[0, 1]): Switch, output each month
        swyrvar (Literal[0, 1]): Output times for overall water and solute
            balances in *.BAL and *.BLC file: choose output at a fixed date
            each year or at different dates
        period (Optional[int]): Fixed output interval
        swres (Optional[Literal[0, 1]]): Switch, reset output interval counter
            each year
        swodat (Optional[Literal[0, 1]]): Switch, extra output dates are given
            in table below
        outdatin (Optional[DateList]): list of specific dates
        datefix (Optional[DayMonth]): fixed date for output
        outdat (Optional[DateList]): specify all output dates
        outfil (str): Generic file name of output files
        swheader (Literal[0, 1]): Print header at the start of each
            balance period
        extensions (list): list of file extensions SWAP should return. 
            Available options are: ["wba", "end", "vap", "bal", "blc", "sba", "ate",
            "bma", "drf", "swb", "ini", "inc", "crp", "str", "irg", "csv", "csv_tz"]
        inlist_csv (Optional[StringList]): list of 
        inlist_csv_tz (Optional[StringList]): list of variables for
            the csv tz output
        swafo (Literal[0, 1, 2]): Switch, output file with
            formatted hydrological data
        swaun (Literal[0, 1, 2]): Switch, output file with
            unformatted hydrological data
        critdevmasbal (Optional[float]): Critical Deviation in
            water balance during PERIOD
        swdiscrvert (Literal[0, 1]): Switch to convert vertical discretization
        numnodnew (Optional[int]): New number of nodes
        dznew (Optional[FloatList]): Thickness of compartments
    """

    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True
    )

    _all_extensions: ClassVar[List[str]] = [
        "wba", "end", "vap", "bal", "blc", "sba", "ate", "bma", "drf", "swb", 
        "ini", "inc", "crp", "str", "irg", "csv", "csv_tz"
    ]
    
    extensions: List[str] = Field(exclude=True)
    
    pathwork: String = Field(default=BASE_PATH, frozen=True)
    pathatm: String = Field(default=BASE_PATH, frozen=True)
    pathcrop: String = Field(default=BASE_PATH, frozen=True)
    pathdrain: String = Field(default=BASE_PATH, frozen=True)
    swscre: Literal[0, 1, 3] = 0
    swerror: Literal[0, 1] = 0

    tstart: date  # convert this to DD-MM-YYYY
    tend: date  # convert this to DD-MM-YYYY

    nprintday: int = Field(default=1, ge=1, le=1440)
    swmonth: Literal[0, 1] = 1
    swyrvar: Literal[0, 1] = 0
    # if swmonth is 0
    period: int | None = Field(default=None, **YEARRANGE)
    swres: Literal[0, 1] | None = None
    swodat: Literal[0, 1] | None = None
    # if swyrvar is 1
    outdatin: DateList | None = None
    datefix: DayMonth | None = None
    outdat: DateList | None = None

    outfil: String = "result"
    swheader: Literal[0, 1] = 0

    inlist_csv: StringList | None = None
    inlist_csv_tz: StringList | None = None
    swafo: Literal[0, 1, 2] = 0
    swaun: Literal[0, 1, 2] = 0
    critdevmasbal: float | None = Field(default=None, **UNITRANGE)
    swdiscrvert: Literal[0, 1] = 0
    numnodnew: int | None = None
    dznew: FloatList | None = None

    @field_validator('extensions')
    def validate_extensions(cls, extensions):
        invalid_extensions = [ext for ext in extensions if ext not in cls._all_extensions]
        if invalid_extensions:
            raise ValueError(f"Invalid extensions: {invalid_extensions}")
        return extensions

    def model_post_init(self, __context):
        for ext in self._all_extensions:
            switch_name = f'sw{ext}'
            setattr(self, switch_name, 1 if ext in self.extensions else 0)

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        if not self.swmonth:
            assert self.period is not None, "period is required when swmonth is 0"
            assert self.swres is not None, "swres is required when swmonth is 0"
            assert self.swodat is not None, "swodat is required when swmonth is 0"
            if self.swodat:
                assert self.outdatin is not None, (
                    "outdatin is required when swodat is 1"
                )

        if self.swyrvar:
            assert self.outdat is not None, "outdat is required when svyrvar is 1"
        else:
            assert self.datefix is not None, "datefix is required when swyrvar is 0"

        if self.swafo in [1, 2] or self.swaun in [1, 2]:
            assert self.critdevmasbal is not None, (
                "critdevmasbal is required when SWAFO = 1 "
            )
            "or 2 or SWAUN = 1 or 2"
            assert self.swdiscrvert, (
                "SWDISCRVERT is required when SWAFO = 1 or 2 or SWAUN = 1 or 2"
            )
        if self.swdiscrvert:
            assert self.numnodnew is not None, (
                "NUMNODNEW is required when SWDISCRVERT = 1"
            )
            assert self.dznew is not None, "DZNEW is required when SWDISCRVERT = 1"

        return self
