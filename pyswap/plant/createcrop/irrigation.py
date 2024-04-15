"""Script for the irrigation part of the .crp file"""
from ...core.utils.basemodel import PySWAPBaseModel
from ...core.utils.fields import Table, DayMonth
from ...core.utils.valueranges import YEARRANGE
from typing import Literal, Optional
from pydantic import Field


class ScheduledIrrigation(PySWAPBaseModel):
    schedule: Literal[0, 1]
    startirr: Optional[DayMonth] = None
    endirr: Optional[DayMonth] = None
    cirrs: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    isuas: Optional[Literal[0, 1]] = None
    tcs: Optional[Literal[1, 2, 3, 4, 5, 6, 7, 8]] = None
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
