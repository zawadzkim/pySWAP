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


from pyswap.components.boundary import *
from pyswap.components.crop import *
from pyswap.components.drainage import *
from pyswap.components.irrigation import *
from pyswap.components.meteorology import *
from pyswap.components.simsettings import *
from pyswap.components.soilwater import *
from pyswap.components.transport import *

__all__ = [
    *boundary.__all__,
    *crop.__all__,
    *drainage.__all__,
    *irrigation.__all__,
    *meteorology.__all__,
    *simsettings.__all__,
    *soilwater.__all__,
    *transport.__all__,
]
