"""Custom field types for pySWAP serialization and deserialization.

The use of custom Annotated fields in combination with Pydantic allows for the
serialization and deserialization of objects to the appropriate format used in
the SWAP. This is particularily useful when Should a new type of field be
implemented, the design should follow the pattern below:

```Python
CustonType = Annotated[
    <native python type>,
    pydantic.AfterValidator(custom_parsing_function),
    pydantic.PlainSerializer(custom_serializer, return_type=<native python type>, when_used="json"),
    pydantic.Field(<custom field parameters>)
    ]
```

Where:

- <native python type>: A native python type of the field that he user has to
    provide (e.g., int).
- pydantic.AfterValidator (optional):
    Pydantic validator runs after the field value passed by the user is
    initially parsed and validated (e.g., for required fields). It then takes a
    custom parsing function as an argument and returns the final value
    compatible with pySWAP serialization. For custom validation functions refer
    to `pyswap.core.parsers` module.
- pydantic.PlainSerializer:
    A serializer in called when Model.model_dump(mode="json") is called.
    Internally in pySWAP this is done in PySWAPBaseModel.model_string() method.
    It takes a custom serialization function as an argument and returns the
    parameter in a string format compatible with SWAP. For custom serializer
    functions, refer to `pyswap.core.serializers` module.
- pydantic.Field:
    In Pydantic Field object is used to define metadata for a field. In pySWAP,
    the context attribute is used to pass additional information to the
    serializer functions.

Then use the custom type in the models:

```Python
class SWAPSection(PySWAPBaseModel):
    field: CustomType
```

Fields in this module:

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
from typing import Annotated, TypeVar

from pandas import DataFrame
from pydantic import AfterValidator, BeforeValidator, Field
from pydantic.functional_serializers import PlainSerializer

from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.parsers import (
    parse_day_month,
    parse_decimal,
    parse_float_list,
    parse_int_list,
    parse_quoted_string,
    parse_string_list,
)
from pyswap.core.serializers import (
    serialize_arrays,
    serialize_day_month,
    serialize_decimal,
    serialize_table,
)

__all__ = [
    "Arrays",
    "DateList",
    "DayMonth",
    "Decimal2f",
    "Decimal3f",
    "Decimal4f",
    "File",
    "FloatList",
    "IntList",
    "String",
    "StringList",
    "Subsection",
    "Table",
]

Table = Annotated[
    DataFrame,
    PlainSerializer(serialize_table, return_type=str, when_used="json"),
    Field(json_schema_extra={"is_annotated_exception_type": True}),
]
"""Serialize pd.DataFrame with headers to a string without leading variable name."""

Arrays = Annotated[
    DataFrame, PlainSerializer(serialize_arrays, return_type=str, when_used="json")
]
"""Serialize pd.DataFrame without headers to a string with leading variable name."""

DayMonth = Annotated[
    date | str,
    AfterValidator(parse_day_month),
    PlainSerializer(serialize_day_month, return_type=str, when_used="json"),
]
"""Serialize date object to a string with just the day and month."""

StringList = Annotated[
    list[str] | str,
    AfterValidator(parse_string_list),
    PlainSerializer(lambda x: f"'{','.join(x)}'", return_type=str, when_used="json"),
]
"""Serialize list of strings to a string with elements separated by commas."""

FloatList = Annotated[
    list[float] | str,
    AfterValidator(parse_float_list),
    PlainSerializer(
        lambda x: " ".join([f"{Decimal(f):.2f}" for f in x]),
        return_type=str,
        when_used="json",
    ),
]
"""Serialize list of floats to a string with elements separated by spaces."""

IntList = Annotated[
    list[int] | str,
    AfterValidator(parse_int_list),
    PlainSerializer(
        lambda x: " ".join([str(f) for f in x]), return_type=str, when_used="json"
    ),
]
"""Serialize list of integers to a string with elements separated by spaces."""

DateList = Annotated[
    list[date],
    PlainSerializer(
        lambda x: "\n" + "\n".join([d.strftime("%Y-%m-%d") for d in x]),
        return_type=str,
        when_used="json",
    ),
]
"""Serialize list of date objects to a string with elements separated by newlines."""

String = Annotated[
    str,
    PlainSerializer(lambda x: f"'{x}'", return_type=str),
    AfterValidator(parse_quoted_string),
]
"""Serialize string to a string with quotation marks."""

File = Annotated[
    PySWAPBaseModel,
    PlainSerializer(lambda x: x.model_string(), return_type=str, when_used="json"),
    Field(json_schema_extra={"is_annotated_exception_type": True}),
]
"""Serialize PySWAPBaseModel to a string."""

SubsectionTypeVar = TypeVar("SubsectionTypeVar", bound=PySWAPBaseModel)

Subsection = Annotated[
    SubsectionTypeVar,
    PlainSerializer(lambda x: x.model_string(), return_type=str),
    Field(json_schema_extra={"is_annotated_exception_type": True}),
]
"""Serialize a nested PySWAPBaseModel to a string."""

Decimal2f = Annotated[
    float | str,
    BeforeValidator(parse_decimal),
    PlainSerializer(serialize_decimal(precision=2), return_type=str, when_used="json"),
]
"""Serialize float to a string with 2 decimal places."""

Decimal3f = Annotated[
    float,
    PlainSerializer(serialize_decimal(precision=3), return_type=str, when_used="json"),
]
"""Serialize float to a string with 3 decimal places."""

Decimal4f = Annotated[
    float,
    PlainSerializer(serialize_decimal(precision=4), return_type=str, when_used="json"),
]
"""Serialize float to a string with 4 decimal places."""
