"""
# Drainage subpackage

Handling drainage settings and creation of the .dra file.

Modules:
    drainage: Holds the drainage settings for the SWAP model.
    drafile: Create the .dra file.
"""

from .drainage import Drainage
from .drafile import (DraFile, DrainageFluxTable, DrainageFormula,
                      DrainageInfiltrationResitance, DraSettings, Flux)
