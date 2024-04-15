from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table, CSVTable
from ..core.utils.files import save_file
from pandas import read_csv, to_datetime
from datetime import datetime as dt
import urllib.request
from pydantic import Field, model_validator
from typing import Optional, Literal
import knmi


class MeteorologicalData(PySWAPBaseModel):
    """Handles creation and operations on meteorological data file for swap.

    Attrs:
        file_meteo (pyswap.core.utils.fields.CSVTable): meteorological data file

    Methods:
        load_from_csv: loads meteorological data from a csv file
        weather_kmni: downloads weather data from KNMI and formats it according to SWAP specification
    """

    file_meteo: Optional[CSVTable] = None

    def load_from_csv(self,
                      csv_path: str,
                      station: str):

        self.file_meteo = read_csv(csv_path, index_col=0)

    def weather_knmi(self,
                     stations: str | list,
                     variables: str | list = [
                         'TEMP', 'PRCP', 'Q', 'UG',  'FG', 'UX', 'UN'],
                     start: str | dt = '20000101',
                     end: str | dt = '20200101',
                     inseason: bool = False):
        """Method for retrieving the meteo data from KNMI API.

        New version uses the KNMI-PY package. Some of the old functionality was moved to csv table serializer.
        """

        if isinstance(stations, str):
            stations = [stations]

        df = knmi.get_day_data_dataframe(stations=stations,
                                         start=start,
                                         end=end,
                                         variables=variables,
                                         inseason=inseason)

        # rename some columns
        required_column_names = {'STN': 'Station',
                                 'TN': 'Tmin',
                                 'TX': 'Tmax',
                                 'UG': 'HUM',
                                 'DR': 'WET',
                                 'FG': 'WIND',
                                 'RH': 'RAIN',
                                 'EV24': 'ETref',
                                 'Q': 'RAD'}

        df = df.rename(columns=required_column_names)

        # recalculation of the parameters
        df[['Tmin', 'Tmax', 'ETref', 'RAIN', 'WIND']] = df[['Tmin', 'Tmax', 'ETref', 'RAIN',
                                                                            'WIND']] * 0.1  # the original unit is 0.1 Unit
        df['WET'] = df['WET'] * \
            0.1 * 24  # the required unit is days

        self.file_meteo = df


class PenmanMonteith(PySWAPBaseModel):
    """Holds the Penman-Monteith settings of the simulation."""

    alt: float = Field(ge=-400.0, le=3000.0)
    altw: float = Field(default=10.0, ge=0.0, le=99.0)
    angstroma: float = Field(default=0.25, ge=0.0, le=1.0)
    angstromb: float = Field(default=0.5, ge=0.0, le=1.0)


class Meteorology(PySWAPBaseModel):
    """Holds the meteorological settings of the simulation."""

    metfil: str
    lat: float = Field(ge=-90, le=90)
    swetr: Literal[0, 1]
    swdivide: Literal[0, 1]
    # TODO: SWRAIN should be optional, but Fortran code evaluates its presence anyway
    swrain: Optional[Literal[0, 1, 2, 3]] = 0
    # TODO: SWETSINE should be optional, but Fortran code evaluates its presence anyway
    swetsine: Literal[0, 1] = 0
    file_meteo: Optional[MeteorologicalData] = Field(
        default=None, repr=False, exclude=True)
    penman_monteith: Optional[PenmanMonteith] = Field(default=None, repr=False)
    swmetdetail: Optional[Literal[0, 1]] = None
    table_rainflux: Optional[Table] = None
    rainfil: Optional[str] = None
    nmetdetail: Optional[int] = Field(default=None, ge=1, le=96)

    @model_validator(mode='after')
    def _validate_meteo_section(self):

        if self.swetr == 1:  # if PM method is NOT used
            assert self.swetsine is not None, "SWETSINE is required when SWETR is 1"
            assert self.swrain is not None, "SWRAIN is required when SWETR is 1"
            if self.swrain == 1:
                assert self.table_rainflux is not None, "RAINFLUX is required when SWRAIN is 1"
            elif self.swrain == 3:
                assert self.rainfil, "RAINFIL is required when SWRAIN is 3"

        else:
            assert self.penman_monteith is not None, "PENMAN-MONTEITH settings are required when SWETR is 0"
            assert self.swmetdetail is not None, "SWMETDETAIL is required when SWETR is 0"
            if self.swmetdetail == 1:
                assert self.nmetdetail is not None, "NMETDETAIL is required when SWMETDETAIL is 1"

    def save_met(self, path: str):
        save_file(
            string=self.file_meteo.model_dump(mode='json')['file_meteo'],
            fname=self.metfil,
            path=path,
            mode='w'
        )
        return 'Meteorological data saved successfully.'
