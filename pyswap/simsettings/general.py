from datetime import date as d
from ..core import PySWAPBaseModel
from ..core import (DayMonth, DateList, StringList, FloatList)
from ..core import YEARRANGE, UNITRANGE
from typing import Literal, Optional
from typing_extensions import Self
from datetime import date as d
from pydantic import Field, model_validator
import platform

IS_WINDOWS = platform.system() == 'Windows'
BASE_PATH = '.\\' if IS_WINDOWS else './'


class GeneralSettings(PySWAPBaseModel):
    """General settings of the simulation.

    !!! todo
        * remove the individual file extension switches and replace with a list of extensions. Make the class
            automatically generate the switches based on the list of extensions.

    Attributes:
        pathwork (str): Path to the working directory
        pathatm (str): Path to folder with weather files
        pathcrop (str): Path to folder with crop files
        pathdrain (str): Path to folder with drainage files
        swscre (Literal[0, 1, 3]): Switch, display progression of simulation run to screen
        swerror (Literal[0, 1]): Switch for printing errors to screen
        tstart (d): Start date of simulation run, give day-month-year
        tend (d): End date of simulation run, give day-month-year
        nprintday (int): Number of output times during a day
        swmonth (Literal[0, 1]): Switch, output each month
        swyrvar (Literal[0, 1]): Output times for overall water and solute balances in *.BAL and *.BLC file: choose output 
            at a fixed date each year or at different dates
        period (Optional[int]): Fixed output interval
        swres (Optional[Literal[0, 1]]): Switch, reset output interval counter each year
        swodat (Optional[Literal[0, 1]]): Switch, extra output dates are given in table below
        outdatin (Optional[DateList]): list of specific dates
        datefix (Optional[DayMonth]): fixed date for output
        outdat (Optional[DateList]): specify all output dates
        outfil (str): Generic file name of output files
        swheader (Literal[0, 1]): Print header at the start of each balance period
        swwba (Literal[0, 1]): Switch, output daily water balance
        swend (Literal[0, 1]): Switch, output end-conditions
        swvap (Literal[0, 1]): Switch, output soil profiles of moisture, solute and temperature
        swbal (Literal[0, 1]): Switch, output file with yearly water balance
        swblc (Literal[0, 1]): Switch, output file with detailed yearly water balance
        swsba (Literal[0, 1]): Switch, output file of daily solute balance
        swate (Literal[0, 1]): Switch, output file with soil temperature profiles
        swbma (Literal[0, 1]): Switch, output file with water fluxes, only for macropore flow
        swdrf (Literal[0, 1]): Switch, output of drainage fluxes, only for extended drainage
        swswb (Literal[0, 1]): Switch, output surface water reservoir, only for extended drainage
        swini (Literal[0, 1]): Switch, output of initial SoilPhysParam and HeatParam
        swinc (Literal[0, 1]): Switch, output of water balance increments
        swcrp (Literal[0, 1]): Switch, output of simple or detailed crop growth model
        swstr (Literal[0, 1]): Switch, output of stress values for wetness, drought, salinity and frost
        swirg (Literal[0, 1]): Switch, output of irrigation gifts
        swcsv (Literal[0, 1]): Switch, csv output
        inlist_csv (Optional[StringList]): list of variables for the csv output
        swcsv_tz (Literal[0, 1]): Switch, csv output with depth
        inlist_csv_tz (Optional[StringList]): list of variables for the csv tz output
        swafo (Literal[0, 1, 2]): Switch, output file with formatted hydrological data
        swaun (Literal[0, 1, 2]): Switch, output file with unformatted hydrological data
        critdevmasbal (Optional[float]): Critical Deviation in water balance during PERIOD
        swdiscrvert (Literal[0, 1]): Switch to convert vertical discretization
        numnodnew (Optional[int]): New number of nodes
        dznew (Optional[FloatList]): Thickness of compartments
    """

    pathwork: str = BASE_PATH
    pathatm: str = BASE_PATH
    pathcrop: str = BASE_PATH
    pathdrain: str = BASE_PATH
    swscre: Literal[0, 1, 3] = 0
    swerror: Literal[0, 1] = 0

    tstart: d  # convert this to DD-MM-YYYY
    tend: d  # convert this to DD-MM-YYYY

    nprintday: int = Field(default=1, ge=1, le=1440)
    swmonth: Literal[0, 1] = 1
    swyrvar: Literal[0, 1] = 0
    # if swmonth is 0
    period: Optional[int] = Field(default=None, **YEARRANGE)
    swres: Optional[Literal[0, 1]] = None
    swodat: Optional[Literal[0, 1]] = None
    # if swyrvar is 1
    outdatin: Optional[DateList] = None
    datefix: Optional[DayMonth] = None
    outdat: Optional[DateList] = None

    outfil: str = "result"
    swheader: Literal[0, 1] = 0
    swwba: Literal[0, 1] = 0
    swend: Literal[0, 1] = 0
    swvap: Literal[0, 1] = 0
    swbal: Literal[0, 1] = 0
    swblc: Literal[0, 1] = 1
    swsba: Literal[0, 1] = 0
    swate: Literal[0, 1] = 0
    swbma: Literal[0, 1] = 0
    swdrf: Literal[0, 1] = 0
    swswb: Literal[0, 1] = 0
    swini: Literal[0, 1] = 0
    swinc: Literal[0, 1] = 0
    swcrp: Literal[0, 1] = 0
    swstr: Literal[0, 1] = 0
    swirg: Literal[0, 1] = 0
    swcsv: Literal[0, 1] = 1
    inlist_csv: Optional[StringList] = None
    swcsv_tz: Literal[0, 1] = 0
    inlist_csv_tz: Optional[StringList] = None
    swafo: Literal[0, 1, 2] = 0
    swaun: Literal[0, 1, 2] = 0
    critdevmasbal: Optional[float] = Field(default=None, **UNITRANGE)
    swdiscrvert: Literal[0, 1] = 0
    numnodnew: Optional[int] = None
    dznew: Optional[FloatList] = None

    @model_validator(mode='after')
    def _validate_model(self) -> Self:

        if not self.swmonth:
            assert self.period is not None, "period is required when swmonth is 0"
            assert self.swres is not None, "swres is required when swmonth is 0"
            assert self.swodat is not None, "swodat is required when swmonth is 0"
            if self.swodat:
                assert self.outdatin is not None, "outdatin is required when swodat is 1"

        if self.swyrvar:
            assert self.outdat is not None, "outdat is required when svyrvar is 1"
        else:
            assert self.datefix is not None, "datefix is required when swyrvar is 0"

        if self.swafo in [1, 2] or self.swaun in [1, 2]:
            assert self.critdevmasbal is not None, "critdevmasbal is required when SWAFO = 1 or 2 or SWAUN = 1 or 2"
            assert self.swdiscrvert, "SWDISCRVERT is required when SWAFO = 1 or 2 or SWAUN = 1 or 2"
        if self.swdiscrvert:
            assert self.numnodnew is not None, "NUMNODNEW is required when SWDISCRVERT = 1"
            assert self.dznew is not None, "DZNEW is required when SWDISCRVERT = 1"

        return self
