"""
General settings for the simulation and settings for the Richards' equation.

Classes:
    GeneralSettings: General settings of the simulation.
    RichardsSettings: Settings for the Richards' equation.
"""

from datetime import date
from typing import ClassVar, Literal
import logging

from pydantic import ConfigDict, Field, model_validator

from pyswap.core.defaults import BASE_PATH
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import YAMLValidatorMixin, SerializableMixin
from pyswap.core.fields import String, StringList, DateList, DayMonth, Arrays
from pyswap.core.valueranges import UNITRANGE, YEARRANGE

__all__ = ["GeneralSettings", "RichardsSettings"]

logger = logging.getLogger(__name__)


class GeneralSettings(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
        outfil (str): Generic file name of output files
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

    model_config = ConfigDict(
        extra="allow", validate_assignment=True, use_enum_values=True
    )

    _all_extensions: ClassVar[list[str]] = [
        "wba",
        "end",
        "vap",
        "bal",
        "blc",
        "sba",
        "ate",
        "bma",
        "drf",
        "swb",
        "ini",
        "inc",
        "crp",
        "str",
        "irg",
        "csv",
        "csv_tz",
    ]

    extensions: list[str] = Field(default_factory=list, exclude=True)

    pathwork: String = Field(default=BASE_PATH, frozen=True)
    pathatm: String = Field(default=BASE_PATH, frozen=True)
    pathcrop: String = Field(default=BASE_PATH, frozen=True)
    pathdrain: String = Field(default=BASE_PATH, frozen=True)
    swscre: Literal[0, 1, 3] = 0
    swerror: Literal[0, 1] = 0

    tstart: date | None = None
    tend: date | None = None

    nprintday: int = Field(default=1, ge=1, le=1440)
    swmonth: Literal[0, 1] | None = None  # 1
    swyrvar: Literal[0, 1] | None = None  # 0
    period: int | None = Field(default=None, **YEARRANGE)
    swres: Literal[0, 1] | None = None
    swodat: Literal[0, 1] | None = None
    outdatin: DateList | None = None
    datefix: DayMonth | None = None
    outdat: DateList | None = None

    outfil: String = "result"
    swheader: Literal[0, 1] = 0

    inlist_csv: StringList | None = None
    inlist_csv_tz: StringList | None = None
    swafo: Literal[0, 1, 2] = 0
    swaun: Literal[0, 1, 2] = 0
    critdevmasbal: float | None = Field(default=None, **UNITRANGE)
    swdiscrvert: Literal[0, 1] = 0
    numnodnew: int | None = None
    dznew: Arrays | None = None

    @model_validator(mode="after")
    def validate_extensions(self):
        invalid_extensions = [
            ext for ext in self.extensions if ext not in self._all_extensions
        ]
        if invalid_extensions:
            raise ValueError(f"Invalid extensions: {invalid_extensions}")
        return self

    def model_post_init(self, __context=None):
        for ext in self._all_extensions:
            switch_name = f"sw{ext}"
            setattr(self, switch_name, 1 if ext in self.extensions else 0)

    def add_extension(self, extension: str, inlist: list = None):
        """Add a new extension to the list and trigger updates.

        Parameters:
            extension (str): Extension to add to the list.
            inlist (list): List of variables for the extension. Applicable when
                extension is 'csv' or 'csv_tz'.
        """
        if extension not in self._all_extensions:
            raise ValueError(f"Invalid extension: {extension}")

        if extension == "csv":
            if not any([self.inlist_csv, inlist]):
                raise ValueError(f"Missing 'inlist_csv' for extension '{extension}'")
            if inlist:
                self.inlist_csv = inlist

        elif extension == "csv_tz":
            if not any([self.inlist_csv_tz, inlist]):
                raise ValueError(f"Missing 'inlist_csv_tz' for extension '{extension}'")
            if inlist:
                self.inlist_csv_tz = inlist

        if extension not in self.extensions:
            self.extensions.append(extension)
            self.model_post_init(None)
            self.model_validate(self)
        else:
            logger.warning(f"Extension '{extension}' is already in the list.")
        return self

    def remove_extension(self, extension: str):
        """
        Remove an extension from the list and trigger updates.
        """
        if extension not in self.extensions:
            raise ValueError(f"Extension '{extension}' is not in the list.")
        self.extensions.remove(extension)

        if extension == "csv":
            self.inlist_csv = None
        elif extension == "csv_tz":
            self.inlist_csv_tz = None

        self.model_post_init(None)
        self.model_validate(self)
        return self


class RichardsSettings(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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

    swkmean: Literal[1, 2, 3, 4, 5, 6] | None = None
    swkimpl: Literal[0, 1] | None = None
    dtmin: float | None = Field(default=0.000001, ge=1e-7, le=0.1)
    dtmax: float | None = Field(default=0.04, ge=0.000001, le=1.0)
    gwlconv: float | None = Field(default=100.0, ge=1e-5, le=1000.0)
    critdevh1cp: float | None = Field(default=0.01, ge=1e-10, le=1e3)
    critdevh2cp: float | None = Field(default=0.1, ge=1e-10, le=1e3)
    critdevponddt: float | None = Field(default=0.0001, ge=1e-6, le=0.1)
    maxit: int | None = Field(default=30, ge=5, le=100)
    maxbacktr: int | None = Field(default=3, ge=1, le=10)
