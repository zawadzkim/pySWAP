"""
## Meteorology module.

This module contains the classes and functions to handle meteorological settings and data for simulations.

Classes:
    MetFile: Meteorological data for the .met file.
    Meteorology: Meteorological settings of the simulation.
    DAILYMETEODATA: Format detailed daily meteo data.
    SHORTINTERVALMETEODATA: Format detailed short interval meteo data.
    DETAILEDRAINFALL: Format detailed rainfall data.
    RAINFLUX: Format rainfall intensity RAINFLUX as function of time TIME.

Functions:
    load_from_csv: Load meteorological data from a CSV file.
    load_from_knmi: Load meteorological data from KNMI API.
"""


from knmi import get_day_data_dataframe, get_hour_data_dataframe
from datetime import datetime as dt
from pandas import read_csv
import pandera as pa
from pandera.typing import Series
from pyswap.core.fields import  CSVTable, String, Table, File
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.valueranges import UNITRANGE, YEARRANGE
from pyswap.core.mixins import FileMixin, YAMLValidatorMixin, SerializableMixin
from pyswap.core.basemodel import BaseTableModel
from pyswap.gis import Location


from pydantic import Field, field_validator, model_validator


from decimal import Decimal
from typing import Literal

__all__ = ["MetFile", "Meteorology", "DAILYMETEODATA", "SHORTINTERVALMETEODATA", "DETAILEDRAINFALL", "RAINFLUX", "load_from_csv", "load_from_knmi"]


class MetFile(PySWAPBaseModel, FileMixin, SerializableMixin):
    """Meteorological data for the .met file.

    This object is created by functions fetching or loading meteorological data
    from various sources. The data is stored as a pandas.DataFrame, but
    is formatted with a custom field serializer of the CSVTable field type.

    Attributes:
        metfil (str): name of the .met file
        content (CSVTable): meteorological data file
    """

    metfil: String
    content: CSVTable | None = Field(default=None, exclude=True)


class Meteorology(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    validation: bool = Field(default=False, exclude=True)


    lat: Decimal | None = Field(default=None, ge=-90, le=90)
    meteo_location: Location | None = Field(default=None, exclude=True)
    swetr: Literal[0, 1]
    swdivide: Literal[0, 1]
    swrain: Literal[0, 1, 2, 3] | None = 0
    swetsine: Literal[0, 1] = 0
    metfile: File | None = Field(default=None, repr=False)
    alt: Decimal | None = Field(default=None, ge=-400.0, le=3000.0)
    altw: Decimal = Field(default=None, ge=0.0, le=99.0)
    angstroma: Decimal = Field(default=None, **UNITRANGE)
    angstromb: Decimal = Field(default=None, **UNITRANGE)
    swmetdetail: Literal[0, 1] | None = None
    table_rainflux: Table | None = None
    rainfil: String | None = None
    nmetdetail: int | None = Field(default=None, ge=1, le=96)

    @property
    def met(self):
        return self.metfile.content.to_csv(index=False, lineterminator="\n")

    @field_validator("altw", "angstroma", "angstromb")
    def set_decimals(cls, v):
        return v.quantize(Decimal("0.00"))

    def model_post_init(self, __context):
        """Set lat, and alt from `meteo_location` if they are not provided."""
        if self.meteo_location:
            self.lat = self.meteo_location.lat
            self.alt = self.meteo_location.alt

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

        print(f"{self.metfile.metfil} saved.")


def load_from_csv(metfil: str, csv_path: str, **kwargs) -> MetFile:
    """Method for loading meteorological data from a CSV file.

    Parameters:
        metfil (str): name of the .met file
        csv_path (str): path to the CSV file
        **kwargs (dict): keyword arguments for pandas.read_csv

    Returns:
        MetFile object.
    """

    return MetFile(metfil=metfil, content=read_csv(csv_path, **kwargs))


def load_from_knmi(
    metfil: str,
    stations: str | list,
    variables: str | list = ["TEMP", "PRCP", "Q", "UG", "FG", "UX", "UN"],
    start: str | dt = "20000101",
    end: str | dt = "20200101",
    frequency: Literal["day", "hour"] = "day",
    inseason: bool = False,
) -> MetFile:
    """Retrieves the meteorological data from KNMI API using knmi-py and
    enforces SWAP required format.

    Parameters:
        metfil (str): name of the .met file
        stations (str | list): station number(s) to retrieve data from
        variables (str | list): variables to retrieve
        start (str | dt): start date of the data
        end (str | dt): end date of the data
        frequency (Literal['day', 'hour']): frequency of the data (day or hour)
        inseason (bool): whether to retrieve in-season data

    Returns:
        MetFile object.
    """

    if isinstance(stations, str):
        stations = [stations]
    if isinstance(variables, str):
        variables = [variables]

    get_func = get_day_data_dataframe if frequency == "day" else get_hour_data_dataframe

    df = get_func(
        stations=stations, start=start, end=end, variables=variables, inseason=inseason
    )

    # rename some columns
    required_column_names = {
        "STN": "Station",
        "TN": "Tmin",
        "TX": "Tmax",
        "UG": "HUM",
        "DR": "WET",
        "FG": "WIND",
        "RH": "RAIN",
        "EV24": "ETref",
        "Q": "RAD",
    }

    df = df.rename(columns=required_column_names)

    # recalculation of the parameters, the original unit is 0.1 Unit
    df[["Tmin", "Tmax", "ETref", "RAIN", "WIND"]] = df[
        ["Tmin", "Tmax", "ETref", "RAIN", "WIND"]
    ].multiply(0.1)

    # The required unit is days
    df["WET"] = df["WET"].multiply(0.1).multiply(24)

    return MetFile(metfil=metfil, content=df)


class DAILYMETEODATA(BaseTableModel):
    """Format detailed daily meteo data.

    validate that the station is in single quotes.
    check if the dd, mm, yyyy columns are already in the
        dataframe. If not, require datetime index and
        parse the datetime index to separate columns.
    format decimals in the variables.
    """

    Station: Series[str]
    DD: Series[str]
    MM: Series[str]
    YYYY: Series[str]
    RAD: Series[float]
    Tmin: Series[float]
    Tmax: Series[float]
    HUM: Series[float]
    WIND: Series[float]
    RAIN: Series[float]
    ETref: Series[float]
    WET: Series[float]


class SHORTINTERVALMETEODATA(BaseTableModel):
    Date: Series[pa.DateTime] # type: ignore
    Record: Series[int] = pa.Field(ge=1, le=10)
    Rad: Series[float]
    Temp: Series[float]
    Hum: Series[float]
    Wind: Series[float]
    Rain: Series[float]


class DETAILEDRAINFALL(BaseTableModel):
    Station: Series[str]
    Day: Series[int]
    Month: Series[int]
    Year: Series[int]
    Time: Series[float]
    Amount: Series[float]


class RAINFLUX(BaseTableModel):
    TIME: Series[int] = pa.Field(**YEARRANGE)
    RAINFLUX: Series[float] = pa.Field(ge=0, le=1000.0)