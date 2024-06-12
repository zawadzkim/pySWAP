""""
Irrigation settings for the SWAP simuluation.

Classes:
    FixedIrrigation: Holds the settings for fixed irrigation.
    ScheduledIrrigation: Holds the settings for scheduled irrigation.
    Irrigation: Holds the irrigation settings of the simulation.
"""
from ..core import PySWAPBaseModel
from ..core import Table, irrigation_schema
from typing import Optional, Literal, Any
from pydantic import model_validator, Field, validator


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
    irgfile: Optional[Any] = Field(
        default=None, repr=False)

    @validator('table_irrigevents')
    def _validate_table_irrigevents(cls, v):
        try:
            validated = irrigation_schema.validate(v)
            return validated
        except Exception as e:
            raise ValueError(f"Invalid irrigation schema: {e}")

    @model_validator(mode='after')
    def _validate_fixed_irrigation(self) -> None:
        if self.swirfix == 1:
            if self.swirgfil:
                assert self.irgfile is not None, "irgfile is required when swirgfil is True"
            else:
                assert self.table_irrigevents is not None, "irrigevents is required when swirgfil is False"


class ScheduledIrrigation(PySWAPBaseModel):
    """Irrigation scheduling settings.

    !!! note
        This class is only used in the .crp file.

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

    schedule: Literal[0, 1]
    fixedirrig: Optional[Any] = None
    scheduledirrig: Optional[Any] = None

    @model_validator(mode='after')
    def _validate_irrigation(self) -> None:
        if self.swirfix == 1:
            assert self.fixedirrig is not None, "fixedirrig is required when swirfix is True"
        if self.schedule == 1:
            assert self.scheduledirrig is not None, "scheduledirrig is required when schedule is True"
