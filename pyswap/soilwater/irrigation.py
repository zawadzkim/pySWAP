from dataclasses import dataclass, field
from datetime import datetime as dt
from ..core.metadata import Metadata
from ..core.dtypes import Section, Subsection
from pandas import DataFrame, read_csv


@dataclass
class IrrigationData:

    metadata: Metadata
    csv_path: str
    irrigation_data: DataFrame | None = None

    def load_from_csv(self, csv_path: str) -> None:

        self.irrigation_data = read_csv(csv_path)

    def __post_init__(self) -> None:
        self.load_from_csv(self.csv_path)


@dataclass
class FixedIrrigation(Subsection):
    """ Holds the settings for fixed irrigation."""

    swirgfil: bool
    irrigevents: DataFrame | None = None
    irgfil: str | None = None

    def __post_init__(self) -> None:
        if self.swirgfil:
            assert self.irgfil is not None, "irgfil is required when swirgfil is True"
        else:
            assert self.irrigevents is not None, "irrigevents is required when swirgfil is False"


@dataclass
class ScheduledIrrigation(Subsection):

    startirr: str
    endirr: str
    cirrs: float
    isuas: int
    phFieldCapacity: float
    tcs: int
    phormc: int | None = None
    swcirrthres: bool | None = None
    cirrthres: float | None = None
    perirrsurp: float | None = None
    irgthreshold: float | None = None
    tcsfix: int | None = None
    dcrit: float | None = None
    irgdayfix: int | None = None
    dvs_tc1: DataFrame | dict[list] | None = None
    dvs_tc2: DataFrame | dict[list] | None = None
    dvs_tc3: DataFrame | dict[list] | None = None
    dvs_tc4: DataFrame | dict[list] | None = None
    dvs_tc5: DataFrame | dict[list] | None = None

    def __post_init__(self) -> None:
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


@dataclass
class Irrigation(Section):
    """ Holds the irrigation settings of the simulation."""
    swirfix: bool
    schedule: bool
    fixedirrig: FixedIrrigation | None = None
    scheduledirrig: ScheduledIrrigation | None = None

    def __post_init__(self) -> None:
        if self.swirfix:
            assert self.fixedirrig is not None, "fixedirrig is required when swirfix is True"
        if self.schedule:
            assert self.scheduledirrig is not None, "scheduledirrig is required when schedule is True"
