"""
General settings for the simulation and settings for the Richards' equation.

Classes:
    GeneralSettings: General settings of the simulation.
    RichardsSettings: Settings for the Richards' equation.
"""

import logging as _logging
from datetime import date as _date
from typing import ClassVar as _ClassVar, Literal as _Literal

from pydantic import ConfigDict as _ConfigDict, Field as _Field, model_validator as _model_validator

from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.defaults import FNAME_OUT as _FNAME_OUT, EXTENSIONS as _EXTENSIONS
from pyswap.core.defaults import BASE_PATH as _BASE_PATH
from pyswap.core.fields import Arrays as _Arrays, DateList as _DateList, DayMonth as _DayMonth, String as _String, StringList as _StringList, Subsection as _Subsection, FloatList as _FloatList, IntList as _IntList
from pyswap.utils.mixins import SerializableMixin as _SerializableMixin, YAMLValidatorMixin as _YAMLValidatorMixin
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE, YEARRANGE as _YEARRANGE

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
        outfil (str): Generic file name of output files. Immutable attribute.
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
    swmonth: _Literal[0, 1] | None = None  # 1
    swyrvar: _Literal[0, 1] | None = None  # 0
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
            raise ValueError(f"Invalid extensions: {invalid_extensions}")
        
        # Create the _ExtensionMixin object without triggering validation
        object.__setattr__(self, 'exts', _ExtensionMixin(**{ext: 1 if ext in self.extensions else 0 for ext in self._all_extensions}))
        return self


class RichardsSettings(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Settings for the Richards' equation.

    Attributes:
        swkmean (Literal[1, 2, 3, 4, 5, 6]): Switch for averaging method of hydraulic conductivity
        swkimpl (Literal[0, 1]): Switch for updating hydraulic conductivity during iteration
        dtmin (float): Minimum timestep [1.d-7..0.1 d]
        dtmax (float): Maximum timestep [dtmin..1 d]
        gwlconv (float): Maximum difference of groundwater level between time steps [1.d-5..1000 cm]
        critdevh1cp (float): Maximum relative difference in pressure heads per compartment [1.0d-10..1.d3]
        critdevh2cp (float): Maximum absolute difference in pressure heads per compartment [1.0d-10..1.d3 cm]
        critdevponddt (float): Maximum water balance error of ponding layer [1.0d-6..0.1 cm]
        maxit (int): Maximum number of iteration cycles [5..100]
        maxbacktr (int): Maximum number of back track cycles within an iteration cycle [1..10]
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
