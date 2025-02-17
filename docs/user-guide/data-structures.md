# Data Structures

The SWAP model input is a simple formatted string saved in a plain ASCII file. There are three main formats/types of input:

- **Key-value pairs**: A variable name followed by an equal sign and a formatted value.
- **Tables**: Rows of data with column names on top. Columns are separated by spaces and lines by newline characters. They do not have a tag (variable name followed by an equal sign).
- **Arrays**: Rows of data without column names on top. Columns are separated by spaces and lines by newline characters. They are preceded by a tag, and the data starts on the next line.

All parameters are grouped into classes representing different components of the SWAP model.

## Classes and attribute types

`pyswap` models (classes or objects) are subclasses of [Pydantic's](https://docs.pydantic.dev/latest/) `BaseModel`. Pydantic is a powerful validation and serialization library that ensures the provided data is of the right type and within the right range. When possible, the input is coerced into the correct format; otherwise, exceptions are raised. Below see an example of a pyswap class definition:

```py
class SnowAndFrost(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow.
        snowinco (Optional[Decimal2f]): Initial snow water equivalent [0..1000 cm].
        teprrain (Optional[Decimal2f]): Temperature above which all
            precipitation is rain [0..10 oC].
        teprsnow (Optional[Decimal2f]): Temperature below which all
            precipitation is snow [-10..0 oC].
        tfroststa (Optional[Decimal2f]): Soil temperature (oC) where reduction
            of water fluxes starts [-10.0..5.0 oC].
        tfrostend (Optional[Decimal2f]): Soil temperature (oC) where reduction
            of water fluxes ends [-10.0..5.0 oC].
    """

    swsnow: _Literal[0, 1] | None = None
    swfrost: _Literal[0, 1] | None = None
    snowinco: _Decimal2f | None = _Field(default=None, ge=0, le=1000)
    teprrain: _Decimal2f | None = _Field(default=None, ge=0, le=10)
    teprsnow: _Decimal2f | None = _Field(default=None, ge=-10, le=0)
    tfroststa: _Decimal2f | None = _Field(default=None, ge=-10, le=5)
    tfrostend: _Decimal2f | None = _Field(default=None, ge=-10, le=5)
```

Attributes of each class generally correspond to the names of the variables in the SWAP input files. Each attribute has an assigned type and validation rules (e.g., lower and upper bounds). Many of these types are custom annotated types with specific serialization and validation rules. These rules tell the class constructor how to interpret a value when it's provided and how to format the data when it is saved to a file.

Below are examples of types with their validation and serialization rules. For more details, see the [validation and serialization section](/reference/developer/#validation_and_serialization).

```py
FloatList = Annotated[
    list[float] | str,
    AfterValidator(parse_float_list),  # (1)!
    PlainSerializer(
        lambda x: " ".join([f"{Decimal(f):.2f}" for f in x]),
        return_type=str,
        when_used="json",  # (2)!
    ),
]
"""Serialize list of floats to a string with elements separated by spaces."""
```

1. Normally, the input should be a list of floats, but if provided as a string, `parse_float_list` will convert it into a list. This is useful when a formatted string from SWAP input files is passed directly. For details, see [reference](/reference/developer/#pyswap.core.parsers.parse_float_list).
2. `PlainSerializer` ensures that during serialization (when input variables are written to a file), the list is converted into a properly formatted string representing the floats with two decimal points using a lambda function.

Here is another example of a field:

```py
Decimal2f = Annotated[
    float | str,
    BeforeValidator(parse_decimal),  # (1)!
    PlainSerializer(serialize_decimal(precision=2), return_type=str, when_used="json"),  # (2)!
]
"""Serialize float to a string with 2 decimal places."""
```

1. [parse_decimal](/reference/developer/#pyswap.core.parsers.parse_decimal) ensures that the string from the input file is actually a float. It removes any Fortran-compatible notation like "d" or "e" to ensure it coerces to a float.
2. [serialize_decimal](/reference/developer/#pyswap.core.serializers.serialize_decimal) ensures that the float is saved to the input file with two decimal points.

## Tables

Tabular data is defined the same way as the key-value pairs by assignmnet to a class attribute. Those attributes are either of type Arrays or Table, depending on what kind or serialization is needed for that particular variable. For both input and output, `pyswap` relies on pandas DataFrames.

### Input

Tabular input is provided as dataframes and shuld be validated before running the model for the presence of certain columns, uper and lower bounds, etc. `pyswap` uses [Pandera](https://pandera.readthedocs.io/en/stable/) library for this, very similar to Pydantic. Currently the way to validate the dataframes is by using `.create()` method of respective schemas. Schemas are essentially classes that in their definition contain the information on which columns are required and what are the required data types.

See below the example of SOILPROFILE schema being defined and then generated using `.create()` method:

```py
class SOILPROFILE(BaseTableModel):
    """Vertical discretization of soil profile

    Attributes:
        ISUBLAY: Series[int]: number of sub layer, start with 1 at soil surface [1..MACP, I].
        ISOILLAY: Series[int]: number of soil physical layer, start with 1 at soil surface [1..MAHO, I].
        HSUBLAY: Series[float]: height of sub layer [0..1.d4 cm, R].
        HCOMP: Series[float]: height of compartments in the sub layer [0.0..1000.0 cm, R].
        NCOMP: Series[int]: number of compartments in the sub layer (Mind NCOMP = HSUBLAY/HCOMP) [1..MACP, I].
    """

    ISOILLAY: Series[int] = pa.Field(ge=1)
    ISUBLAY: Series[int] = pa.Field(ge=1)
    HSUBLAY: Series[float] = pa.Field(ge=0.0, le=1.0e4)
    HCOMP: Series[float] = pa.Field(ge=0.0, le=1.0e3)
    NCOMP: Series[int] = pa.Field(ge=1)
```

This is how you create the table:

```py
import pyswap as psp  # (1)!

soil_profile = psp.components.soilwater.SOILPROFILE.create({
    "ISUBLAY": [1, 2, 3, 4],  # (2)!
    "ISOILLAY": [1, 1, 2, 2],
    "HSUBLAY": [10.0, 20.0, 30.0, 140.0],
    "HCOMP": [1.0, 5.0, 5.0, 10.0],
    "NCOMP": [10, 4, 6, 14],
})
```

1. Table schemas are imported from the same component group as the class they should be assigned to. So `SOILPROFILE` will be imported from `soilwater` component.
2. Here, for example, if we tried to set one of the elements in `ISUBLAY` column to 0, we would get an error.

### Output

All output from the model is captured in a `Result` object. This includes requested output ascii files (e.g., .blc) and CSV files. The CSV output files are automatically converted to a pandas DataFrame with DateTime index.

!!! note

    ASCII output files, like .blc will be deprecated in the future version of SWAP and pyswap.
