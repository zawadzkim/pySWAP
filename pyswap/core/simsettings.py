from datetime import date as d
from .utils.basemodel import PySWAPBaseModel
from .utils.fields import (DayMonth, DateList, StringList, FloatList)
from pathlib import Path
from typing import Literal, Optional
from datetime import date as d
from pydantic import Field, model_validator


class SimSettings(PySWAPBaseModel):
    """Holds the general settings of the simulation."""

    pathwork: str = './'
    pathatm: str = './'
    pathcrop: str = './'
    pathdrain: str = './'
    swscre: Literal[0, 1, 3] = 0
    swerror: Literal[0, 1] = 1

    tstart: d  # convert this to DD-MM-YYYY
    tend: d  # convert this to DD-MM-YYYY

    nprintday: int = Field(default=1, ge=1, le=1440)
    swmonth: Literal[0, 1] = 1
    swyrvar: Literal[0, 1] = 0
    # if swmonth is 0
    period: Optional[int] = Field(default=None, ge=0, le=366)
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
    swblc: Literal[0, 1] = 0
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
    critdevmasbal: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    swdiscrvert: Literal[0, 1] = 0
    numnodnew: Optional[int] = None
    dznew: Optional[FloatList] = None

    @model_validator(mode='after')
    def _validate_model(self):

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
