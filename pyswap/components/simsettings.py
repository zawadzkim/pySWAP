# mypy: disable-error-code="call-overload, misc, override, type-arg"

"""General settings for the simulation and settings for the Richards' equation.

Classes:
    GeneralSettings: General settings of the simulation.
    RichardsSettings: Settings for the Richards' equation.
"""

import logging as _logging
from datetime import date as _date
from typing import (
    ClassVar as _ClassVar,
    Literal as _Literal,
)

from pydantic import (
    ConfigDict as _ConfigDict,
    Field as _Field,
    model_validator as _model_validator,
)

from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import (
    BASE_PATH as _BASE_PATH,
    EXTENSIONS as _EXTENSIONS,
    FNAME_OUT as _FNAME_OUT,
)
from pyswap.core.fields import (
    Arrays as _Arrays,
    DayMonth as _DayMonth,
    String as _String,
    StringList as _StringList,
    Subsection as _Subsection,
)
from pyswap.core.valueranges import (
    UNITRANGE as _UNITRANGE,
    YEARRANGE as _YEARRANGE,
)
from pyswap.utils.mixins import (
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = ["GeneralSettings", "RichardsSettings"]

logger = _logging.getLogger(__name__)


class _ExtensionMixin(_PySWAPBaseModel, _SerializableMixin):
    """Handle creation of the switches through direct assignment and list."""

    swwba: _Literal[1, 0] | None = _Field(default=None, validation_alias="wba")
    swend: _Literal[1, 0] | None = _Field(default=None, validation_alias="end")
    swvap: _Literal[1, 0] | None = _Field(default=None, validation_alias="vap")
    swbal: _Literal[1, 0] | None = _Field(default=None, validation_alias="bal")
    swblc: _Literal[1, 0] | None = _Field(default=None, validation_alias="blc")
    swsba: _Literal[1, 0] | None = _Field(default=None, validation_alias="sba")
    swate: _Literal[1, 0] | None = _Field(default=None, validation_alias="ate")
    swbma: _Literal[1, 0] | None = _Field(default=None, validation_alias="bma")
    swdrf: _Literal[1, 0] | None = _Field(default=None, validation_alias="drf")
    swswb: _Literal[1, 0] | None = _Field(default=None, validation_alias="swb")
    swini: _Literal[1, 0] | None = _Field(default=None, validation_alias="ini")
    swinc: _Literal[1, 0] | None = _Field(default=None, validation_alias="inc")
    swcrp: _Literal[1, 0] | None = _Field(default=None, validation_alias="crp")
    swstr: _Literal[1, 0] | None = _Field(default=None, validation_alias="str")
    swirg: _Literal[1, 0] | None = _Field(default=None, validation_alias="irg")
    swcsv: _Literal[1, 0] | None = _Field(default=None, validation_alias="csv")
    swcsv_tz: _Literal[1, 0] | None = _Field(default=None, validation_alias="csv_tz")


class GeneralSettings(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """General settings of the simulation.

    Attributes:
        pathwork (str): Path to the working directory. Immutable attribute.
        pathatm (str): Path to folder with weather files. Immutable attribute.
        pathcrop (str): Path to folder with crop files. Immutable attribute.
        pathdrain (str): Path to folder with drainage files. Immutable attribute.
        swscre (Literal[0, 1, 3]): Switch, display progression of simulation
            run to screen:
            * 0 - no display to screen
            * 1 - display water balance components
            * 2 - display daynumber
        swerror (Literal[0, 1]): Switch for printing errors to screen:
            * 0 - no error messages
            * 1 - print error messages
        tstart (str): Start date of simulation run.
        tend (str): End date of simulation run.
        nprintday (int): Number of output times during a day
        swmonth (Literal[0, 1]): Switch, output each month:
            * 0 - No output each month, choose period, swres or swodat
            * 1 - Output each month
        period (Optional[int]): Fixed output interval in days
        swres (Optional[Literal[0, 1]]): Switch, reset output interval counter
            each year:
            * 0 - No
            * 1 - Yes
        swodat (Optional[Literal[0, 1]]): Switch, extra output dates.
            * 0 - No extra output dates
            * 1 - Extra output dates (outdatin)
        outdatin (Optional[DateList]): list of specific dates.
        swyrvar (Literal[0, 1]): Output times for overall water and solute
            balances in *.BAL and *.BLC file: choose output at a fixed date
            each year or at different dates
            * 0 - each year output at the same date (datefix)
            * 1 - output at specific dates (outdat)
        datefix (Optional[DayMonth]): Fixed date for output
        outdat (Optional[DateList]): Specify all output dates
        outfil (str): Generic file name of output files. Immutable attribute.
        swheader (Literal[0, 1]): Print header at the start of each
            balance period:
            * 0 - No header
            * 1 - Print header
        extensions (list): List of file extensions SWAP should return.
            Available options are: ["wba", "end", "vap", "bal", "blc", "sba", "ate",
            "bma", "drf", "swb", "ini", "inc", "crp", "str", "irg", "csv", "csv_tz"]
        inlist_csv (Optional[StringList]): List of variables for the csv output.
            Available options are: TODO
        inlist_csv_tz (Optional[StringList]): List of variables over depth for
            the csv tz output. Available options are:
        swafo (Literal[0, 1, 2]): Switch, output file with formatted hydrological data:
            * 0 - no output
            * 1 - output to a file named *.AFO
            * 2 - output to a file named *.BFO
        swaun (Literal[0, 1, 2]): Switch, output file with unformatted hydrological data:
            * 0 - no output
            * 1 - output to a file named *.AUN
            * 2 - output to a file named *.BUN
        critdevmasbal (Optional[float]): Critical Deviation in
            water balance during PERIOD [0.0 .. 1.0 cm]
        swdiscrvert (Literal[0, 1]): Switch to convert vertical discretization:
            * 0 - no conversion
            * 1 - convert vertical discretization
        numnodnew (Optional[int]): New number of nodes.
        dznew (Optional[FloatList]): New thickness of compartments.
    """

    model_config = _ConfigDict(
        validate_assignment=True, use_enum_values=True, extra="ignore"
    )
    _all_extensions: _ClassVar[list[str]] = _EXTENSIONS
    extensions: list[str] = _Field(default_factory=list, exclude=True)
    exts: _Subsection[_ExtensionMixin] | None = None

    pathwork: _String = _Field(default=_BASE_PATH, frozen=True)
    pathatm: _String = _Field(default=_BASE_PATH, frozen=True)
    pathcrop: _String = _Field(default=_BASE_PATH, frozen=True)
    pathdrain: _String = _Field(default=_BASE_PATH, frozen=True)
    swscre: _Literal[0, 1, 3] = 0
    swerror: _Literal[0, 1] = 0

    tstart: _date | None = None
    tend: _date | None = None

    nprintday: int = _Field(default=1, ge=1, le=1440)
    swmonth: _Literal[0, 1] = 1
    swyrvar: _Literal[0, 1] = 0
    period: int | None = _Field(default=None, **_YEARRANGE)
    swres: _Literal[0, 1] | None = None
    swodat: _Literal[0, 1] | None = None
    outdatin: _Arrays | None = None
    datefix: _DayMonth | None = None
    outdat: _Arrays | None = None

    outfil: _String = _Field(default=_FNAME_OUT, frozen=True)
    swheader: _Literal[0, 1] = 0

    inlist_csv: _StringList | None = None
    inlist_csv_tz: _StringList | None = None
    swafo: _Literal[0, 1, 2] = 0
    swaun: _Literal[0, 1, 2] = 0
    critdevmasbal: float | None = _Field(default=None, **_UNITRANGE)
    swdiscrvert: _Literal[0, 1] = 0
    numnodnew: int | None = None
    dznew: _Arrays | None = None

    @_model_validator(mode="after")
    def validate_extensions(self):
        invalid_extensions = [
            ext for ext in self.extensions if ext not in self._all_extensions
        ]
        if invalid_extensions:
            msg = f"Invalid extensions: {', '.join(invalid_extensions)}"
            raise ValueError(msg)

        # Create the _ExtensionMixin object without triggering validation
        object.__setattr__(
            self,
            "exts",
            _ExtensionMixin(
                **{
                    ext: 1 if ext in self.extensions else 0
                    for ext in self._all_extensions
                }
            ),
        )
        return self


class RichardsSettings(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings for the Richards' equation.

    Attributes:
        swkmean (Literal[1, 2, 3, 4, 5, 6]): Switch for averaging method of hydraulic conductivity:
            * 1 - unweighted arithmic mean
            * 2 - weighted arithmic mean
            * 3 - unweighted geometric mean
            * 4 - weighted geometric mean
            * 5 - unweighted harmonic mean
            * 6 - weighted harmonic mean
        swkimpl (Literal[0, 1]): Switch for updating hydraulic conductivity during iteration:
            * 0 - no update
            * 1 - update
        dtmin (float): Minimum timestep [1.0e-7 .. 0.1 d]
        dtmax (float): Maximum timestep [dtmin .. 1 d]
        gwlconv (float): Maximum difference of groundwater level between time steps [1.0e-5 .. 1.0e3 cm]
        critdevh1cp (float): Maximum relative difference in pressure heads per compartment [1.0e-10 .. 1.0e3]
        critdevh2cp (float): Maximum absolute difference in pressure heads per compartment [1.0e-10 .. 1.0e3 cm]
        critdevponddt (float): Maximum water balance error of ponding layer [1.0e-6 .. 0.1 cm]
        maxit (int): Maximum number of iteration cycles [5 .. 100]
        maxbacktr (int): Maximum number of back track cycles within an iteration cycle [1 .. 10]
    """

    swkmean: _Literal[1, 2, 3, 4, 5, 6] | None = None
    swkimpl: _Literal[0, 1] | None = None
    dtmin: float | None = _Field(default=0.000001, ge=1e-7, le=0.1)
    dtmax: float | None = _Field(default=0.04, ge=0.000001, le=1.0)
    gwlconv: float | None = _Field(default=100.0, ge=1e-5, le=1000.0)
    critdevh1cp: float | None = _Field(default=0.01, ge=1e-10, le=1e3)
    critdevh2cp: float | None = _Field(default=0.1, ge=1e-10, le=1e3)
    critdevponddt: float | None = _Field(default=0.0001, ge=1e-6, le=0.1)
    maxit: int | None = _Field(default=30, ge=5, le=100)
    maxbacktr: int | None = _Field(default=3, ge=1, le=10)
