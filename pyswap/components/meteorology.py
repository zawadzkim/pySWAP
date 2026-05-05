# mypy: disable-error-code="call-overload, misc, operator"
# the operator error was raised bacause of Pydantic validators. The current
# implementation is correct, so it was not the priority to fix.


"""Meteorology settings and data.

This module contains the classes and functions to handle meteorological settings and data for simulations.

Classes:
    MetFile: Meteorological data for the .met file.
    Meteorology: Meteorological settings of the simulation.

Functions:
    load_from_csv: Load meteorological data from a CSV file.
    load_from_knmi: Load meteorological data from KNMI API.
"""

from datetime import datetime as _datetime
from typing import (
    Literal as _Literal,
)

from knmi import (
    get_day_data_dataframe as _get_day_data_dataframe,
    get_hour_data_dataframe as _get_hour_data_dataframe,
)
from numpy import exp as _exp
from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import (
    DAILYMETEODATA,
    DETAILEDRAINFALL,
    RAINFLUX,
    SHORTINTERVALMETEODATA,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Decimal2f as _Decimal2f,
    File as _File,
    String as _String,
    Table as _Table,
)
from pyswap.core.io.io_csv import load_csv
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE
from pyswap.gis import Location as _Location
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "DAILYMETEODATA",
    "DETAILEDRAINFALL",
    "RAINFLUX",
    "SHORTINTERVALMETEODATA",
    "MetFile",
    "Meteorology",
    "metfile_from_csv",
    "metfile_from_knmi",
]


class MetFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Meteorological data for the .met file.

    This object is created by functions fetching or loading meteorological data
    from various sources. The data is stored as a pandas.DataFrame, but
    is formatted with a custom field serializer of the CSVTable field type.

    Attributes:
        metfil (str): name of the .met file
        content (CSVTable): meteorological data file
    """

    # None, because the extension has to be added to metfil
    _extension: bool = _PrivateAttr(default=None)

    metfil: _String
    content: _Table | None = _Field(default=None, exclude=True)


class Meteorology(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Meteorological settings of the simulation.

    !!! note
        SWRAIN and SWETSINE should be optional,
        but Fortran code evaluates its presence anyway. They are set to
        0 by default.


    Attributes:
        meteo_location (Location): a point GIS object. If provided, lat
            and alt must not be provided. By default they are overwritten.
        lat (Decimal): latitude of the meteo station [degrees].
        swetr (int): Switch type of weather data for
            potential evapotranspiration:

            * 0 - Use basic weather data and apply Penman-Monteith equation.
            * 1 - Use reference evapotranspiration data in combination with
                crop factors.

        swdivide (int): Switch for distribution of E and T. Defaults to 0:

            * 0 - Based on crop and soil factors.
            * 1 - Based on direct application of Penman-Monteith.

        swmetdetail (int): Switch for time interval of evapotranspiration and
            rainfall weather data:

            * 0 - Daily data.
            * 1 - Subdaily data.

        swrain (int): Switch for use of actual rainfall intensity,
            defaults to 0:

            * 0 - Use daily rainfall amounts.
            * 1 - Use daily rainfall amounts + mean intensity.
            * 2 - Use daily rainfall amounts + duration.
            * 3 - Use detailed rainfall records (dt < 1 day), as supplied in
                separate file.

        swetsine (int): Switch, distribute daily Tp and Ep according to
            sinus wave, default to 0:

            * 0 - No distribution.
            * 1 - Distribute Tp and Ep according to sinus wave.

        metfile (MetFile): MetFile model containing meteorological data to
            be saved to .met file.
        alt (Decimal): Altitude of the meteo station [m].
        altw (Decimal): Altitude of the wind [m].
        angstroma (Decimal): Fraction of extraterrestrial radiation reaching
            the earth on overcast days.
        angstromb (Decimal): Additional fraction of extraterrestrial radiation
            reaching the earth on clear days.
        table_rainflux (Table): rainfall intensity RAINFLUX as function
            of time TIME.
        rainfil (str): file name of file with detailed rainfall data.
        nmetdetail (int): Number of weather data records each day.

    Properties:
        met: Returns the string representation of the met file.

    Methods:
        write_met: Writes the .met file.
    """

    lat: _Decimal2f | None = _Field(default=None, ge=-90, le=90)
    meteo_location: _Location | None = _Field(default=None, exclude=True)
    swetr: _Literal[0, 1] | None = None
    swdivide: _Literal[0, 1] | None = None
    swrain: _Literal[0, 1, 2, 3] | None = 0
    swetsine: _Literal[0, 1] = 0
    metfile: _File | None = _Field(default=None, repr=False)
    alt: _Decimal2f | None = _Field(default=None, ge=-400.0, le=3000.0)
    altw: _Decimal2f = _Field(default=None, ge=0.0, le=99.0)
    angstroma: _Decimal2f = _Field(default=None, **_UNITRANGE)
    angstromb: _Decimal2f = _Field(default=None, **_UNITRANGE)
    swmetdetail: _Literal[0, 1] | None = None
    table_rainflux: _Table | None = None
    rainfil: _String | None = None
    nmetdetail: int | None = _Field(default=None, ge=1, le=96)

    @property
    def met(self):
        return self.metfile.content.to_csv(index=False, lineterminator="\n")

    def model_post_init(self, __context=None):
        """Set lat, and alt from `meteo_location` if Location object is provided."""
        if self.meteo_location:
            self.lat = self.meteo_location.lat
            self.alt = self.meteo_location.alt

        self._validation = True
        self.validate_with_yaml()
        self._validation = False

    def write_met(self, path: str):
        """Write the .met file.

        !!! note

            in this function the extension is not passed because
            swp file requires the metfile parameter to be passed already with
            the extension.

        Parameters:
            path (str): Path to the file.
        """

        self.metfile.save_file(string=self.met, fname=self.metfile.metfil, path=path)


def metfile_from_csv(metfil: str, csv_path: str, **kwargs) -> MetFile:
    """Method for loading daily meteorological data from a CSV file.

    !!! note

        The CSV file must contain the following columns:
        station, dd, mm, yyyy, tmin, tmax, hum, wet, wind, rain, etref, rad

    Parameters:
        metfil (str): name of the .met file
        csv_path (str): path to the CSV file
        **kwargs (dict): keyword arguments for pandas.read_csv

    Returns:
        MetFile object.
    """
    # Create table from csv
    df = load_csv(csv_path, **kwargs)
    table = DAILYMETEODATA.create(data=df.to_dict())

    # Make sure Station column has quotes
    table.loc[:, "STATION"] = table.STATION.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x
    )

    return MetFile(metfil=metfil, content=table)


def metfile_from_knmi(
    metfil: str,
    stations: str | list,
    start: str | _datetime = "20000101",
    end: str | _datetime = "20200101",
    frequency: _Literal["day", "hour"] = "day",
    # inseason: bool = False,  # Do not use, will cause missing data crashing SWAP
) -> MetFile:
    """Retrieves the meteorological data from KNMI API using knmi-py and
    enforces SWAP required format.

    !!! note:
        Currently, only daily data can be retrieved.

    Parameters:
        metfil (str): name of the .met file
        stations (str | list): station number(s) to retrieve data from
        start (str | dt): start date of the data
        end (str | dt): end date of the data
        frequency (Literal['day', 'hour']): frequency of the data (day or hour)

    Returns:
        MetFile object.
    """

    if not isinstance(stations, list):
        stations = [stations]

    # variables to retrieve and their SWAP name
    variables = {
        "STN": "STATION",
        "Q": "RAD",
        "TN": "TMIN",
        "TX": "TMAX",
        "UG": "HUM",
        "FG": "WIND",
        "RH": "RAIN",
        "EV24": "ETREF",
        "DR": "WET",
    }

    # Retrieve data
    get_func = (
        _get_day_data_dataframe if frequency == "day" else _get_hour_data_dataframe
    )

    df = get_func(
        stations=stations,
        start=start,
        end=end,
        variables=list(variables.keys())[1:],
    )

    # Making separate columns for day, month, year
    df.insert(1, "DD", df.index.day)
    df.insert(2, "MM", df.index.month)
    df.insert(3, "YYYY", df.index.year)

    # Rename columns and drop index
    df = df.reset_index(drop=True)
    df = df.rename(columns=variables)

    # Set -1 to zero in RAIN and SUNH columns (rain or sun hours < 0.05 mm and h respectively)
    df["RAIN"] = df["RAIN"].apply(lambda x: 0 if x == -1 else x)

    # Changing unit of data (see knmi documentation)
    factor = {
        "RAD": 10,  # Convert from J/cm2 to kJ/m2
        "TMIN": 0.1,  # Unit: Convert from 1 to 0.1 degC
        "TMAX": 0.1,  # Convert from 1 to 0.1 degC
        "HUM": 0.01,  # Convert from % to fraction
        "WIND": 0.1,  # Convert from 1 to 0.1 m/s
        "RAIN": 0.1,  # Convert from 1 to 0.1 mm
        "ETREF": 0.1,  # Convert from 1 to 0.1 mm
        "WET": (0.1 / 24),  # Convert from 0.1 h to fraction of day
    }
    df = df.apply(lambda x: x * factor.get(x.name, 1))

    # Convert from fraction to kPa according to Allen et al. (1998)
    es_min = 0.6108 * _exp(17.27 * df["TMIN"].values / (df["TMIN"].values + 237.3))
    es_max = 0.6108 * _exp(17.27 * df["TMAX"].values / (df["TMAX"].values + 237.3))
    df["HUM"] = (es_min + es_max) / 2 * df["HUM"]

    # Make sure Station column has quotes
    df["STATION"] = df["STATION"].apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x
    )

    # Make MeteoData table
    table = DAILYMETEODATA.create(data=df.to_dict())

    return MetFile(metfil=metfil, content=table)
