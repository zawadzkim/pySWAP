"""
Getting and formatting meteorological data for SWAP similation.

Classes:
    MetFile: meteorological data for the .met file

Functions:
    load_from_csv: loading meteorological data from a CSV file
    load_from_knmi: retrieving meteorological data from KNMI API
"""

from typing import Optional, Literal
from pandas import read_csv
from datetime import datetime as dt
from knmi import get_day_data_dataframe, get_hour_data_dataframe
from ..core import PySWAPBaseModel
from ..core import CSVTable
from pydantic import Field


class MetFile(PySWAPBaseModel):
    """Meteorological data for the .met file.

    This object is created by functions fetching or loading meteorological data
    from various sources. The data is stored as a pandas.DataFrame, but is formatted 
    with a custom field serializer of the CSVTable field type.

    Attributes:
        metfil (str): name of the .met file
        content (CSVTable): meteorological data file
    """

    metfil: str
    content: Optional[CSVTable] = Field(default=None, exclude=True)


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


def load_from_knmi(metfil: str,
                   stations: str | list,
                   variables: str | list = [
                       'TEMP', 'PRCP', 'Q', 'UG',  'FG', 'UX', 'UN'],
                   start: str | dt = '20000101',
                   end: str | dt = '20200101',
                   frequency: Literal['day', 'hour'] = 'day',
                   inseason: bool = False) -> MetFile:
    """Retrieves the meteorological data from KNMI API using knmi-py.

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

    return MetFile(metfil=metfil, content=df)
