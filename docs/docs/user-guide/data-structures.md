# Data structures

pySWAP heavily relies on pandas DataFrames, but also defines a number of its own data structures. Here is a summary of the data types and when to use them.

## Tables

Generally pySWAP classes are validated before creation. Variable ranges and types are checked. The same goes for DataFrames, but their validation is a little bit less straighforward. Below you see a class representing the table of initial pressure head as a function of soil depth.

```py
class INIPRESSUREHEAD(BaseModel):
    """Initial pressure head [cm, R] as a function of soil layer [1..N, I].

    Attributes:
        ZI: Series[int]: soil depth [-1.d5..0 cm, R].
        H: Series[float]: Initial soil water pressure head [-1.d10..1.d4 cm, R].
    """

    ZI: Series[int] = pa.Field(ge=-1.0e5, le=0.0)
    H: Series[float] = pa.Field(ge=-1.0e10, le=1.0e4)
```

This is how you create the table:

```py
from pyswap.irrigation import IRRIGATION


irrigation_events = IRRIGATION.create({
    'IRDATE': ['2017-04-01', '2017-05-01', '2017-06-01', '2017-07-01', '2017-08-01'],
    'IRDEPTH': [0.0, 0.0, 0.0, 0.0, 0.0],
    'IRCONC': [0.0, 0.0, 0.0, 0.0, 0.0],
    'IRTYPE': [0, 0, 0, 0, 0],
})

```

`irrigation_events` variable now stores a validated pandas DataFrame. it means that pandera will check if all required columns are there and whether the column types are correct. In case, for example, string is passed for the datetime type, pandera will try to coerce the string to a datetime format. If that is not possible, an error is raised:

```py
from pyswap.irrigation import IRRIGATION


irrigation_events = IRRIGATION.create({
    'IRDATE': ['2017-13-32', '2017-05-01', '2017-06-01', '2017-07-01', '2017-08-01'],
    'IRDEPTH': [0.0, 0.0, 0.0, 0.0, 0.0],
    'IRCONC': [0.0, 0.0, 0.0, 0.0, 0.0],
    'IRTYPE': [0, 0, 0, 0, 0],
})

# output:
# >>>     SchemaError: Error while coercing 'IRDATE' to type datetime64[ns]: Could not coerce <class 'pandas.core.series.Series'> data_container into type datetime64[ns]:
# >>>     index failure_case
# >>> 0      0   2017-13-32

```
