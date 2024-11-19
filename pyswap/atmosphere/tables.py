import pandera as pa
from pandera.typing import Series

from ..core import YEARRANGE
from ..core.tablevalidation import BaseTableModel


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
    Date: Series[pa.DateTime]
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
