# Core module

Core module contains sevarl modules and submodules.

## Metadata

Contains class holding metadata for the project.

NOTE: As of end of 2023, the metadata object is only used in the .SWP file to provide basic information about the project.

Use example:

```Python
from pyswap.core.metadata import Metadata

meta = Metadata(author="John Doe",
                institution="University of Somewhere",
                email="john.doe@somewhere.com",
                project_name="Test",
                swap_ver="4.0")
```

## Simulation settings

Main simulation settings are stored in `SimSettings` class. Arguments of SimSettings are also predefined objects:

- `Environment`
- `SimPeriod`
- `OutputDates`
- `OutputFiles`

### `Environment` class

## Exceptions

Contains exception classes for easier code debugging.

## Model

The main class representing a SWAP model. The main model object is designed to set the parameters in the "GENERAL" section of the .swp file. That includes the main settings of the simulation.
