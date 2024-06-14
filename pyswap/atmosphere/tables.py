from ..core.tablevalidation import BaseModel
from pandera.typing import Series
import pandera as pa

class DAILYMETEODATA(BaseModel):
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

class SHORTINTERVALMETEODATA(BaseModel):
    Date: Series[pa.DateTime]
    Record: Series[int] = pa.Field(ge=1, le=10)
    Rad: Series[float]
    Temp: Series[float]
    Hum: Series[float]
    Wind: Series[float]
    Rain: Series[float]

class DETAILEDRAINFALL(BaseModel):
    Station: Series[str]
    Day: Series[int]
    Month: Series[int]
    Year: Series[int]
    Time: Series[float]
    Amount: Series[float]