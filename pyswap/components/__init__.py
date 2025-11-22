"""SWAP model components.

This module contains the components of the pySWAP model. Each component is
implemented as a class that inherits from Pydantic BaseModel. The components
are used to store the input data for the model and to provide methods to
convert the data to the format required by the SWAP model.
"""

from pyswap.components import (
    boundary,
    crop,
    drainage,
    irrigation,
    meteorology,
    simsettings,
    soilwater,
    transport,
)
from pyswap.components.metadata import Metadata

__all__ = [
    "Metadata",
    "boundary",
    "crop",
    "drainage",
    "irrigation",
    "metadata",
    "meteorology",
    "simsettings",
    "soilwater",
    "transport",
]
