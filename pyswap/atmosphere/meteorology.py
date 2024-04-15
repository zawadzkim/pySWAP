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

    # def weather_knmi(self,
    #                  stations: str | list,
    #                  variables: str | list = [
    #                      'TEMP', 'PRCP', 'Q', 'UG',  'FG', 'UX', 'UN'],
    #                  start: str | dt = '20000101',
    #                  end: str | dt = '20200101',
    #                  inseason: bool = False):

    #     if isinstance(stations, str):
    #         stations = [stations]

    #     self.file_meteo = knmi.get_day_data_dataframe(stations=stations,
    #                                                   start=start,
    #                                                   end=end,
    #                                                   variables=variables,
    #                                                   inseason=inseason)

    def weather_knmi(self,
                     station: str,
                     start_date: str = '20000101',
                     end_date: str = '20200101',
                     parameters: str = 'TEMP:PRCP:Q:UG:FG:UX:UN'):
        """
        Downloads data from kmni and formats it according to SWAP specification for .met file.

        Data from KNMI is easily accessible through URL download.
        Parameters originally have units as follows:
        FG: Daily average windspeed (in 0.1 m/s)
        TN: Minimum temperature (in 0.1 degrees Celsius)
        TX: Maximum temperature (in 0.1 degrees Celsius)
        Q: Global radiation (in J/cm2)
        DR: Duration of precipitation (in 0.1 hours)
        RH: Rainfall (in 0.1 mm) (-1 for <0.05 mm)
        UG: Daily average relative humidity (as a percentage)
        TODO: the URL does not cut the downloaded records at the 'end' date.

        :param stations: list of stations from which data will be downloaded
        :param start_date: start date of downloaded timeseries
        :param end_date: end date of downloaded timeseries
        :param parameters: required meteorological parameters
        :return: formated dataframe of weather records for the .met file
        """

        # Define the parameters for the URL
        stns = station
        params = parameters
        start = start_date
        end = end_date

        # warning: there is comment about data inhomogeneity in the data header; not sure what to do about it.
        # Concatenate the URL and send request
        site_url = 'https://www.daggegevens.knmi.nl/klimatologie/daggegevens?' + \
                   'stns=' + stns + '&' + \
                   'vars=' + params + '&' + \
                   'start=' + start + '&' + \
                   'end=' + end + '.csv'

        num_header_rows = sum(1 for line in urllib.request.urlopen(
            site_url) if line.decode().startswith('#'))

        # Last commented line was the header.
        weather_df = read_csv(site_url, skiprows=num_header_rows - 1)
        weather_df.columns = [item.replace(
            '#', '').strip() for item in weather_df.columns.tolist()]

        # the date has to be in three separate columns. New column names according to docs.
        weather_df['YYYYMMDD'] = to_datetime(
            weather_df['YYYYMMDD'], format='%Y%m%d')
        weather_df['DD'] = weather_df['YYYYMMDD'].dt.day
        weather_df['MM'] = weather_df['YYYYMMDD'].dt.month
        weather_df['YYYY'] = weather_df['YYYYMMDD'].dt.year
        weather_df.drop(columns=['YYYYMMDD', 'T10N', 'TG'], inplace=True)

        required_column_names = {'STN': 'Station',
                                 'TN': 'Tmin',
                                 'TX': 'Tmax',
                                 'UG': 'HUM',
                                 'DR': 'WET',
                                 'FG': 'WIND',
                                 'RH': 'RAIN',
                                 'EV24': 'ETref',
                                 'Q': 'RAD'}

        weather_df = weather_df.rename(columns=required_column_names)

        required_order = ['Station', 'DD', 'MM', 'YYYY', 'RAD',
                          'Tmin', 'Tmax', 'HUM', 'WIND', 'RAIN', 'ETref', 'WET']
        weather_df = weather_df.reindex(columns=required_order)

        # recalculation of the parameters
        weather_df[['Tmin', 'Tmax', 'ETref', 'RAIN', 'WIND']] = weather_df[['Tmin', 'Tmax', 'ETref', 'RAIN',
                                                                            'WIND']] * 0.1  # the original unit is 0.1 Unit
        weather_df['WET'] = weather_df['WET'] * \
            0.1 * 24  # the required unit is days

        self.file_meteo = weather_df


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
