"""Custom field types used for serilization in the model_dump(mode='json').

Other parameters:
    Table (DataFrame): A DataFrame object serialized as a string with just
        the headers and the data.
    Arrays (DataFrame): A DataFrame object serialized as a string with just
        the columns of data (no headers),
        but with the variable name in front (e.g., FLUXTB = 0.0 0.0/n 1.0 1.0 )
    CSVTable (DataFrame): A DataFrame object serialized as a string with
        the headers and data in CSV format,
        specifically tailored for the .met file format.
    DayMonth (d): A date object serialized as a string with just the day and
        month (e.g., '01 01').
    StringList (List[str]): A list of strings serialized as a string with
        the elements separated by commas, enclosed
        in quotation marks (e.g., 'string1, string2, string3').
    FloatList (List[float]): A list of floats serialized as a string with
        the elements separated by spaces.
    DateList (List[d]): A list of date objects serialized as a string with
        the elements separated by newlines.
    Switch (bool | int): A boolean or integer serialized as
        an integer (0 or 1).
    ObjectList (list): A list of objects serialized as a string with
        the elements separated by newlines.
"""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pandas import DataFrame
from pydantic.functional_serializers import PlainSerializer
from pydantic import Field

from pyswap.core.serializers import (
    serialize_arrays,
    serialize_csv_table,
    serialize_object_list,
    serialize_table,
)
from pyswap.core.basemodel import PySWAPBaseModel

Table = Annotated[
    DataFrame,
    PlainSerializer(serialize_table, return_type=str, when_used="json"),
    Field(json_schema_extra={"is_annotated_exception_type": True})
]
"""Serialize pd.DataFrame with headers to a string without leading variable name."""

Arrays = Annotated[
    DataFrame,
    PlainSerializer(serialize_arrays, return_type=str, when_used="json")
]
"""Serialize pd.DataFrame without headers to a string with leading variable name."""

CSVTable = Annotated[
    DataFrame,
    PlainSerializer(
        lambda x: serialize_csv_table(x), return_type=str, when_used="json"
    ),
]

DayMonth = Annotated[
    date,
    PlainSerializer(
        lambda x: f"{x.strftime('%d %m')}", return_type=str, when_used="json"
    ),
]

StringList = Annotated[
    list[str],
    PlainSerializer(lambda x: f"'{','.join(x)}'", return_type=str, when_used="json"),
]

FloatList = Annotated[
    list[float],
    PlainSerializer(
        lambda x: " ".join([f"{Decimal(f):.2f}" for f in x]),
        return_type=str,
        when_used="json",
    ),
]

IntList = Annotated[
    list[int],
    PlainSerializer(
        lambda x: " ".join([str(f) for f in x]), return_type=str, when_used="json"
    ),
]

DateList = Annotated[
    list[date],
    PlainSerializer(
        lambda x: "\n" + "\n".join([d.strftime("%Y-%m-%d") for d in x]),
        return_type=str,
        when_used="json",
    ),
]

Switch = Annotated[
    bool | int, PlainSerializer(lambda x: int(x), return_type=int, when_used="json")
]

ObjectList = Annotated[
    list,
    PlainSerializer(serialize_object_list, return_type=str, when_used="json"),
]

String = Annotated[str, PlainSerializer(lambda x: f"'{x}'", return_type=str)]

File = Annotated[
    PySWAPBaseModel,
    PlainSerializer(lambda x: x.model_string(), return_type=str, when_used="json"),
    Field(json_schema_extra={"is_annotated_exception_type": True})
    ]

Subsection = Annotated[
    PySWAPBaseModel,
    PlainSerializer(lambda x: x.model_string(), return_type=str),
    Field(json_schema_extra={"is_annotated_exception_type": True})
]