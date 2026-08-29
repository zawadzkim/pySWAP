# mypy: disable-error-code="call-overload, misc, override"
# - override was raised on model_string, because the methods do not share the
#   same signature. This was not a proirity to fix.
"""Irrigation settings for the SWAP simuluation.

Classes:
    IrgFile: The irrigation file.
    FixedIrrigation: Fixed irrigation settings.
    ScheduledIrrigation: Irrigation scheduling settings.

Functions:
    irg_from_csv: Load the irrigation file from a CSV file.
"""

from pathlib import Path as _Path
from typing import Literal as _Literal

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
    model_validator as _model_validator,
)

from pyswap.components.tables import IRRIGEVENTS, SSDIEVENTS
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import FNAME_IN as _FNAME_IN
from pyswap.core.fields import (
    DayMonth as _DayMonth,
    Decimal2f as _Decimal2f,
    String as _String,
    Table as _Table,
)
from pyswap.core.valueranges import YEARRANGE as _YEARRANGE
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = ["IRRIGEVENTS", "SSDIEVENTS", "FixedIrrigation", "ScheduledIrrigation"]


class FixedIrrigation(
    _PySWAPBaseModel, _SerializableMixin, _FileMixin, _YAMLValidatorMixin
):
    """Fixed irrigation settings in the .swp file.

    Attributes:
        swirfix (Literal[0, 1]): Switch for fixed irrigation applications
        swirgfil (Literal[0, 1]): Switch for separate file with fixed irrigation applications
        irrigevents (Optional[Table]):
        irgfil (Optional[str]):
        swssdi (Optional[Literal[0, 1]]): Switch for subsurface drip irrigation
            (SSDI) — a source term at depth in the Richards equation
            (SWAP >= 4.2.0; documented in the SWAP manual section 11.2.4).
        ssdi_file (Optional[str]): Name of the SSDI input file, written next to
            the .swp file (default 'swap.ssdi').
        ssdi_schedule (Optional[Literal[0]]): SSDI scheduling mode; only the
            fixed-events mode (0) is currently supported.
        ssdievents (Optional[Table]): SSDIEVENTS table with the dated
            applications (date, rate [mm/h], amount [mm]).
        ssdi_z (Optional[float]): Application depth [-100..0 cm].
    """

    _extension = _PrivateAttr(default="irg")

    swirfix: _Literal[0, 1] | None = None
    swirgfil: _Literal[0, 1] | None = None
    irgfil: _String = _Field(default=_FNAME_IN, frozen=True)
    irrigevents: _Table | None = None
    swssdi: _Literal[0, 1] | None = None
    ssdi_file: _String | None = None
    ssdi_schedule: _Literal[0] | None = None
    ssdievents: _Table | None = None
    ssdi_z: _Decimal2f | None = _Field(default=None, ge=-100.0, le=0.0)

    # Fields that belong to the separate SSDI file, not to the .swp section.
    _ssdi_content = {"ssdi_schedule", "ssdievents", "ssdi_z"}

    @_model_validator(mode="after")
    def _ssdi_defaults(self):
        if self.swssdi == 1:
            if self.ssdi_file is None:
                self.ssdi_file = "swap.ssdi"
            if self.ssdi_schedule is None:
                self.ssdi_schedule = 0
        return self

    def model_string(self, **kwargs) -> str:
        """Override the model_string to handle optional file generation.

        Return the full section if swirgfil is set to 1, otherwise, irrigevents
        is excluded from the string and saved in a separate .irg file.
        The SSDI content fields always go to the separate SSDI file; only the
        SWSSDI switch and the file name appear in the .swp section.
        """
        exclude = set(self._ssdi_content)
        if self.swirgfil == 1:
            exclude.add("irrigevents")
        return super().model_string(exclude=exclude, **kwargs)

    @property
    def irg(self):
        return super().model_string(include={"irrigevents"})

    @property
    def ssdi(self):
        """The content of the separate SSDI input file."""
        return super().model_string(include=self._ssdi_content)

    def write_ssdi(self, path: _Path):
        """Write the SSDI events to the separate SSDI file.

        This method is only available when the swssdi attribute is set to 1.

        Parameters:
            path (Path): Path to the directory where the SSDI file will be
                saved.
        """
        if self.swssdi != 1:
            msg = "SSDI data are not set to be written to a separate file."
            raise ValueError(msg)

        with open(_Path(path) / self.ssdi_file, "w", encoding="ascii") as f:
            f.write(self.ssdi)

    def write_irg(self, path: _Path):
        """Write irrigation data to .irg file.

        This method is only available when the swirgfil attribute is set to 1.

        Parameters:
            path (Path): Path to the directory where the .irg file will be
                saved.
        """
        if self.swirgfil != 1:
            msg = "Irrigation data are not set to be written to a .irg file."
            raise ValueError(msg)

        self.save_file(string=self.irg, fname=self.irgfil, path=path)


class ScheduledIrrigation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Irrigation scheduling settings in the .crp file.

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

    schedule: _Literal[0, 1] | None = None
    startirr: _DayMonth | None = None
    endirr: _DayMonth | None = None
    cirrs: float | None = _Field(default=None, ge=0.0, le=100.0)
    isuas: _Literal[0, 1] | None = None
    tcs: _Literal[1, 2, 3, 4, 6, 7, 8] | None = None

    phfieldcapacity: float | None = _Field(default=None, ge=-1000.0, le=0.0)
    irgthreshold: float | None = _Field(default=None, ge=0.0, le=20.0)
    dcrit: float | None = _Field(default=None, ge=-100.0, le=0.0)
    swcirrthres: _Literal[0, 1] | None = None
    cirrthres: float | None = _Field(default=None, ge=0.0, le=100.0)
    perirrsurp: float | None = _Field(default=None, ge=0.0, le=100.0)
    tcsfix: _Literal[0, 1] | None = None
    irgdayfix: int | None = _Field(default=None, **_YEARRANGE)
    dcs: _Literal[0, 1] | None = None
    dcslim: _Literal[0, 1] | None = None
    irgdepmin: float | None = _Field(default=None, ge=0.0, le=100.0)
    irgdepmax: float | None = _Field(default=None, ge=0.0, le=1.0e7)
    tc1tb: _Table | None = None
    tc2tb: _Table | None = None
    tc3tb: _Table | None = None
    tc4tb: _Table | None = None
    tc7tb: _Table | None = None
    tc8tb: _Table | None = None
    dc1tb: _Table | None = None
    dc2tb: _Table | None = None
