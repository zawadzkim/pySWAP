from dataclasses import dataclass, field
from datetime import date as d
from .dtypes import DateList, FloatList, StringList, Section, Subsection
from pathlib import Path
from .dtypes import DateList
from typing import List
from datetime import date as d


@dataclass
class Environment(Subsection):
    """
    Environment of a SWAP model. Always has to be attached to a SWAP model object.

    Parameters
    ----------
    pathwork : Path, optional
        The path to the working directory.
    pathatm : Path, optional
        The path to the atmospheric data directory.
    pathcrop : Path, optional
        The path to the crop data directory.
    pathdrain : Path, optional
        The path to the drainage data directory.
    swscre : int, optional
        The screen output level.
    swerror : int, optional
        The error output level.
    """
    pathwork: Path = field(default=Path.cwd())
    pathatm: Path = field(default=Path.cwd())
    pathcrop: Path = field(default=Path.cwd())
    pathdrain: Path = field(default=Path.cwd())
    swscre: int = field(default=0)
    swerror: int = field(default=0)

    def __post_init__(self):
        assert isinstance(
            self.pathwork, Path), "pathwork must be a Path object"
        assert isinstance(self.pathatm, Path), "pathatm must be a Path object"
        assert isinstance(
            self.pathcrop, Path), "pathcrop must be a Path object"
        assert isinstance(
            self.pathdrain, Path), "pathdrain must be a Path object"


@dataclass
class SimPeriod(Subsection):
    """
    Simulation period of a SWAP model. Always has to be attached to a SWAP model object.

    Parameters
    ----------
    tstart : datetime.date
        The start date of the simulation period.
    tend : datetime.date
        The end date of the simulation period.
    """
    tstart: d
    tend: d

    def __post_init__(self):
        assert isinstance(
            self.tstart, d), "tstart must be a datetime.date object"
        assert isinstance(self.tend, d), "tend must be a datetime.date object"


@dataclass
class OutputDates(Subsection):
    """Output dates of a SWAP model. Always has to be attached to a SWAP model object"""

    nprintday: int = field(default=1)
    swmonth: bool = field(default=True)
    swyrvar: bool = field(default=False)
    period: int | None = None
    swres: bool | None = None
    swodat: bool | None = None
    outdatin: List[d] | None = None
    datefix: d | None = None
    outdat: List[d] | None = None

    def __post_init__(self):
        assert self.nprintday is not None, "nprintday is required"
        assert self.nprintday > 0 and self.nprintday < 1441, "nprintday must be between 1 and 1440"
        assert self.swmonth is not None, "swmonth is required"
        assert self.swyrvar is not None, "swyrvar is required"
        if not self.swmonth:
            assert self.period is not None, "period is required when swmonth is False"
            assert self.period > 0 and self.period < 367, "period must be between 0 and 366"
            assert self.swres is not None, "swres is required when swmonth is False"
            assert self.swodat is not None, "swodat is required when swmonth is False"
        if self.swyrvar:
            assert self.outdatin is not None, "outdatin is required when svyrvar is True"

        if self.swyrvar:
            assert self.datefix is not None, "datefix is required when swyrvar is True"
            self.datefix = d.strptime(self.datefix, "%Y-%m-%d")
        else:
            assert self.outdat is not None, "outdat is required when swyrvar is True"

    def __setattr__(self, name, value):
        if name == "outdatin" and value is not None:
            value = DateList(value)
        elif name == "outdat" and value is not None:
            value = DateList(value)
        super().__setattr__(name, value)


@dataclass
class OutputFiles(Subsection):
    outfil: str = field(default="result")
    swheader: bool = False
    swwba: bool = False
    swend: bool = False
    swvap: bool = False
    swbal: bool = False
    swblc: bool = False
    swsba: bool = False
    swate: bool = False
    swbma: bool = False
    swdrf: bool = False
    swswb: bool = False
    swini: bool = False
    swinc: bool = False
    swcrp: bool = False
    swstr: bool = False
    swirg: bool = False
    swcsv: bool = True
    inlist_csv: StringList | None = field(
        default=None, metadata={"required": "swcsv"})
    swcsv_tz: bool = False
    inlist_csv_tz: StringList | None = field(
        default=None, metadata={"required": "swcsv_tz"})
    swafo: int = 0
    swaun: int = 0
    critdevmasbal: float = None
    swdiscrvert: bool = False
    numnodnew: int = None
    dznew: FloatList | None = None

    def __post_init__(self):
        if self.swcsv:
            assert self.inlist_csv is not None, "inlist_csv is required when swcsv is True"
        if self.swcsv_tz:
            assert self.inlist_csv_tz is not None, "inlist_csv_tz is required when swcsv_tz is True"
        if self.swafo in [1, 2] or self.swaun in [1, 2]:
            assert self.critdevmasbal is not None, "critdevmasbal is required when SWAFO = 1 or 2 or SWAUN = 1 or 2"
            assert self.swdiscrvert, "SWDISCRVERT is required when SWAFO = 1 or 2 or SWAUN = 1 or 2"
        if self.swdiscrvert:
            assert self.numnodnew is not None, "NUMNODNEW is required when SWDISCRVERT = 1"
            assert self.dznew is not None, "DZNEW is required when SWDISCRVERT = 1"

    def __setattr__(self, name, value):
        if name == "inlist_csv" and value is not None:
            value = StringList(value)
        elif name == "inlist_csv_tz" and value is not None:
            value = StringList(value)
        elif name == "dznew" and value is not None:
            value = FloatList(value)
        super().__setattr__(name, value)


@dataclass
class SimSettings(Section):
    """Holds the general settings of the simulation."""
    environment: Environment
    simulation_period: SimPeriod
    output_dates: OutputDates
    output_files: OutputFiles
