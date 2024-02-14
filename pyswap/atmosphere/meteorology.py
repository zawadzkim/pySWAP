from dataclasses import dataclass, field
from ..core.dtypes import Section, Subsection, Table
from ..core.metadata import Metadata
from ..core.utils import save_file
from pandas import DataFrame, read_csv, to_datetime
from datetime import datetime as dt
import urllib.request


@dataclass
class MeteorologicalData:
    """
    Handles creation and operations on meteorological data file for swap.

    Currently, only .met file is supported.
    For Belgium, there is no possibility to obtain the precipitation duration for the model. There is only
    max intensity. Therefore, the WET parameter is always set to -99.0 for simulations using Belgian data.
    TODO: check if the meteodata has all the required columns
    TODO: include a method to download data from KMI
    """

    required_header = ['Station', 'DD', 'MM', 'YYYY', 'RAD', 'Tmin', 'Tmax',
                       'HUM', 'WIND', 'RAIN', 'ETref', 'WET']

    metadata: Metadata
    station: str = None
    meteodata: DataFrame | None = None

    def load_from_csv(self,
                      csv_path: str,
                      station: str,
                      station_lon: float,
                      station_lat: float,
                      station_alt: float):

        self.meteodata = read_csv(csv_path)
        self.station = station

        self.met_file_params.update({'{STATION}': str(station),
                                     '{PROJECT_NAME}': self.metadata.project_name,
                                     '{FILENAME}': f'{station}',
                                     '{LON}': station_lon,
                                     '{LAT}': station_lat,
                                     '{ALT}': station_alt,
                                     '{AUTHOR}': f'{self.metadata.author}, {self.metadata.email}',
                                     '{TIMESTAMP}': dt.now().strftime("%Y-%m-%d %H:%M:%S")})

    def weather_kmni(self,
                     stations: str = '377',
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
        stns = stations
        vars = parameters
        start = start_date
        end = end_date

        # warning: there is comment about data inhomogeneity in the data header; not sure what to do about it.
        # Concatenate the URL and send request
        site_url = 'https://www.daggegevens.knmi.nl/klimatologie/daggegevens?' + \
                   'stns=' + stns + '&' + \
                   'vars=' + vars + '&' + \
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

        self.meteodata = weather_df

    @staticmethod
    def save_metfile(meteodata: DataFrame,
                     fname: str,
                     path: str):

        save_file(string=meteodata.to_string(index=False), path=path, extension='met', fname=fname,
                  mode='w')


@dataclass
class PenmanMonteith(Subsection):
    """Holds the Penman-Monteith settings of the simulation."""

    alt: float
    altw: float = field(default=10.0)
    angstroma: float = field(default=0.25)
    angstromb: float = field(default=0.5)
    swmetdetail: bool = field(default=False)
    nmetdetail: int | None = field(default=None)

    def __post_init__(self):
        assert -400 <= self.alt <= 3000, "ALT must be between -400 and 3000 meters"
        assert 0 <= self.altw <= 99, "ALTW must be between 0 and 99 meters"
        assert 0 <= self.angstroma <= 1, "ANGSTROMA must be between 0 and 1"
        assert 0 <= self.angstromb <= 1, "ANGSTROMB must be between 0 and 1"
        if self.swmetdetail:
            assert 1 <= self.nmetdetail <= 96, "NMETDETAIL must be between 1 and 96 when SWMETDETAIL is True"


@dataclass
class Meteorology(Section):
    """Holds the meteorological settings of the simulation."""

    metfil: str
    lat: float
    swetr: bool
    swdivide: bool
    meteo_data: MeteorologicalData = field(repr=False)
    swetsine: bool | None = field(default=None)
    swrain: int | None = field(default=None)
    rainfil: str | None = field(default=None)
    rainflux: DataFrame | dict[list] | None = field(default=None)
    penman_monteith: PenmanMonteith | None = field(default=None)

    def __post_init__(self):

        self.metfil += '.met' if not self.metfil.endswith('.met') else ''

        assert -90 <= self.lat <= 90, "LAT must be between -90 and 90 degrees"
        if not self.swetr:
            assert self.penman_monteith is not None, "PENMAN-MONTEITH settings are required when SWETR is False"
        else:
            assert self.swetsine is not None, "SWETSINE is required when SWETR is True"
            assert self.swrain in [0, 1, 2, 3], "SWRAIN must be 0, 1, 2, or 3"
            if self.swrain == 1:
                assert self.rainflux is not None, "RAINFLUX is required when SWRAIN is 1"
            elif self.swrain == 3:
                assert self.rainfil, "RAINFIL is required when SWRAIN is 3"

    def __setattr__(self, name, value):
        """Overrides the default __setattr__ method to check the validity of the new attributes."""
        if name == "penman_monteith" and value is not None:
            assert isinstance(
                value, PenmanMonteith), "penman_monteith must be an instance of PenmanMonteith"
        elif name == "rainflux" and value is not None:
            assert isinstance(value, dict) or isinstance(
                value, DataFrame), "rainflux must be an instance of dict or DataFrame"
            if isinstance(value, dict):
                value = Table(value)
        super().__setattr__(name, value)
