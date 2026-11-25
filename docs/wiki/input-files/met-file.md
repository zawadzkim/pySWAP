---
search:
  boost: 0.5
---

# .MET

Originally, the meteorological data was passed to SWAP in files that had extensions equal to the last three digits of the year. However, the option to use one file (csv-like) with .met extension seems to be the best choice for simplicity. Therefore, for now, pySWAP only allows to use the .met file.

Depending on the selected option, the .met file will have a different set of headers.

## Using your own weather data

You do not need a SWAP-formatted file or a testcase to provide weather data: `MetFile` takes a pandas DataFrame with your own daily records, one row per day, with the columns `STATION, DD, MM, YYYY, RAD, TMIN, TMAX, HUM, WIND, RAIN, ETREF, WET` (units and the missing-value convention are listed in the `MetFile` docstring).

```python
import pandas as pd
import pyswap as psp

obs = pd.read_csv("my_station.csv", parse_dates=["date"])  # your own data

df = pd.DataFrame({
    "STATION": "'my_station'",
    "DD": obs["date"].dt.day,
    "MM": obs["date"].dt.month,
    "YYYY": obs["date"].dt.year,
    "RAD": obs["radiation_kj_m2"],
    "TMIN": obs["tmin"],
    "TMAX": obs["tmax"],
    "HUM": obs["vapour_pressure_kpa"],
    "WIND": obs["wind_2m"],
    "RAIN": obs["rain_mm"],
    "ETREF": -99.9,  # let SWAP compute ETref (Penman-Monteith, swetr=0)
    "WET": 0.0,
})

meteo = psp.components.Meteorology(
    metfile=psp.components.MetFile(metfil="my_station.met", content=df),
    swetr=0,
    # ... other settings
)
```
