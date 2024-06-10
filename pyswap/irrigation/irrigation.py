""""
Irrigation settings for the SWAP simuluation.

Classes:
    FixedIrrigation: Holds the settings for fixed irrigation.
    ScheduledIrrigation: Holds the settings for scheduled irrigation.
    Irrigation: Holds the irrigation settings of the simulation.
"""
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from typing import Optional, Literal, Any
from pydantic import model_validator, Field
from .irgfile import IrrigationFile


class FixedIrrigation(PySWAPBaseModel):
    """ Holds the settings for fixed irrigation.

    Attributes:
        swirgfil (Literal[0, 1]): 
        table_irrigevents (Optional[Table]):
        irgfil (Optional[str]):
        irrigationdata (Optional[IrrigationFile]):
    """

    swirgfil: Literal[0, 1]
    table_irrigevents: Optional[Table] = None
    irgfil: Optional[str] = None
    irrigationdata: Optional[IrrigationFile] = Field(
        default=None, repr=None, exclude=True)

    @model_validator(mode='after')
    def _validate_fixed_irrigation(self) -> None:
        if self.swirgfil:
            assert self.irgfil is not None, "irgfil is required when swirgfil is True"
            assert self.irrigationdata is not None, "irrigationdata is required when swirgfil is True"
        else:
            assert self.table_irrigevents is not None, "irrigevents is required when swirgfil is False"


class ScheduledIrrigation(PySWAPBaseModel):
    """ Holds the settings for scheduled irrigation.

    Attributes:
        startirr (str):
        endirr (str):
        cirrs (float):
        isuas (int):
        phFieldCapacity (float):
        tcs (int):
        phormc (Optional[int]):
        swcirrthres (Optional[bool]):
        cirrthres (Optional[float]):
        perirrsurp (Optional[float]):
        irgthreshold (Optional[float]):
        tcsfix (Optional[int]):
        dcrit (Optional[float]):
        irgdayfix (Optional[int]):
        dvs_tc1 (Optional[Table]):
        dvs_tc2 (Optional[Table]):
        dvs_tc3 (Optional[Table]):
        dvs_tc4 (Optional[Table]):
        dvs_tc5 (Optional[Table]):
    """

    startirr: str
    endirr: str
    cirrs: float
    isuas: int
    phFieldCapacity: float
    tcs: int
    phormc: Optional[int] = None
    swcirrthres: Optional[bool] = None
    cirrthres: Optional[float] = None
    perirrsurp: Optional[float] = None
    irgthreshold: Optional[float] = None
    tcsfix: Optional[int] = None
    dcrit: Optional[float] = None
    irgdayfix: Optional[int] = None
    dvs_tc1: Optional[Table] = None
    dvs_tc2: Optional[Table] = None
    dvs_tc3: Optional[Table] = None
    dvs_tc4: Optional[Table] = None
    dvs_tc5: Optional[Table] = None

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


class Irrigation(PySWAPBaseModel):
    """ Holds the irrigation settings of the simulation.

    Attributes:
        swirfix (Literal[0, 1]):
        schedule (Literal[0, 1]):
        fixedirrig (Optional[Any]):
        scheduledirrig (Optional[Any]):
    """

    swirfix: Literal[0, 1]
    schedule: Literal[0, 1]
    fixedirrig: Optional[Any] = None
    scheduledirrig: Optional[Any] = None

    @model_validator(mode='after')
    def _validate_irrigation(self) -> None:
        if self.swirfix == 1:
            assert self.fixedirrig is not None, "fixedirrig is required when swirfix is True"
        if self.schedule == 1:
            assert self.scheduledirrig is not None, "scheduledirrig is required when schedule is True"
