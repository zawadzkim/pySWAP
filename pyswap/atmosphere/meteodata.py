"""
meteodata.py contains a model and functions for getting and formatting the meteorological data that
goes into the .met file required by the SWAP model.
"""

from typing import Optional, Literal
from pandas import read_csv
from datetime import datetime as dt
from knmi import get_day_data_dataframe, get_hour_data_dataframe
from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import CSVTable


class MeteoData(PySWAPBaseModel):
    """Meteorological data for the .met file.

    This object is created by functions fetching or loading meteorological data
    from various sources. The data is stored as a pandas.DataFrame, but is formatted 
    with a custom field serializer of the pyswap.core.utils.fields.CSVTable field type.

    Attrs:
        content (pyswap.core.utils.fields.CSVTable): meteorological data file
    """

    content: Optional[CSVTable] = None


def load_from_csv(csv_path: str, **kwargs) -> MeteoData:
    """Method for loading meteorological data from a CSV file.

    Args:
        csv_path (str): path to the CSV file
        **kwargs: keyword arguments for pandas.read_csv

    Returns:
        pyswap.core.utils.meteodata.MeteoData object.
    """

    return MeteoData(content=read_csv(csv_path, index_col=0, **kwargs))


def load_from_knmi(stations: str | list,
                   variables: str | list = [
                       'TEMP', 'PRCP', 'Q', 'UG',  'FG', 'UX', 'UN'],
                   start: str | dt = '20000101',
                   end: str | dt = '20200101',
                   frequency: Literal['day', 'hour'] = 'day',
                   inseason: bool = False) -> MeteoData:
    """Retrieves the meteorological data from KNMI API using knmi-py.

    Args:
        stations (str | list): station number(s) to retrieve data from
        variables (str | list): variables to retrieve
        start (str | dt): start date of the data
        end (str | dt): end date of the data
        frequency (Literal['day', 'hour']): frequency of the data (day or hour)
        inseason (bool): whether to retrieve in-season data

    Returns:
        pyswap.core.utils.meteodata.MeteoData object.
    """

    if isinstance(stations, str):
        stations = [stations]
    if isinstance(variables, str):
        variables = [variables]

    get_func = get_day_data_dataframe if frequency == 'day' else get_hour_data_dataframe

    df = get_func(stations=stations,
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

    return MeteoData(content=df)
