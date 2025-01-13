"""Functions to fine tune the serializatino of pySWAP objects to SWAP
formatted ASCII.

More complex serialization logic which would be unwieldy to implement directly
in the Annotated field definitions (pyswap.core.fields module) as lambda
functions are defined in the serializers module (pyswap.core.serializers). These
are functions that convert objects to strings in the valid SWAP format.

Serializers in this module:
    serialize_table: Convert a DataFrame to a string.
    serialize_arrays: Convert a DataFrame to a string without headers and
        newline in front.
    serialize_csv_table: Convert a DataFrame to a string in CSV format.
    serialize_object_list: Convert a list of objects to a string.
    serialize_day_month: Convert a date object to a string with just the day
        and month.

"""

from pandas import DataFrame, DatetimeIndex

from pyswap.core.basemodel import PySWAPBaseModel
from datetime import date


def serialize_table(table: DataFrame) -> str:
    """Convert the DataFrame to a string.

    Arguments:
        table: The DataFrame to be serialized.

    Result:
        >>> ' A  B\n 1  4\n 2  5\n 3  6\n'
    """
    return f"{table.to_string(index=False)}\n"


def serialize_arrays(table: DataFrame) -> str:
    """Convert the DataFrame to a string without headers and newline in front.

    Arguments:
        table: The DataFrame to be serialized.

    Result:
        >>> 'ARRAYS = \n1 4\n2 5\n3 6\n\n'
    """
    return f"\n{table.to_string(index=False, header=False)}\n"


def serialize_csv_table(table: DataFrame) -> str:
    """Convert the DataFrame to a string in CSV format.

    This serializer is specifically tailored to output the data in the
    format of the ,met files used in SWAP.

    Arguments:
        table: The DataFrame to be serialized.
    """
    if isinstance(table.index, DatetimeIndex):
        table["DD"] = table.index.day
        table["MM"] = table.index.month
        table["YYYY"] = table.index.year
        required_order = [
            "Station",
            "DD",
            "MM",
            "YYYY",
            "RAD",
            "Tmin",
            "Tmax",
            "HUM",
            "WIND",
            "RAIN",
            "ETref",
            "WET",
        ]
        table = table[required_order]

    table.loc[:, "Station"] = table.Station.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x
    )
    return table.to_csv(index=False, lineterminator="\n")


def serialize_object_list(list: list[PySWAPBaseModel]) -> str:
    """Serialize a list of objects to a string.

    This is mostly used to convert pyswap.Section objects to a string.

    Arguments:
        list: The list of objects to be serialized.
    """
    string = ""
    for item in list:
        string += item.model_string()

    return string


def serialize_day_month(value: date) -> str:
    """Serialize a date object to a string with just the day and month.

    Arguments:
        value: The date object to be serialized.

    Result:
        >>> '01 01'
    """
    return value.strftime("%d %m")


def serialize_decimal(precision: int):
    def decimal_serializer(v, info):
        return f"{round(v, precision):.{precision}f}"

    return decimal_serializer
