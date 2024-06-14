"""
# Plant subpackage

Crop settings and files for the SWAP simulation.

Modules:
    crop: The crop settings.
    crpfile: The crop file.
    create_crp_tables: Experimental module with functions to create crop tables.
"""

from .crop import *
from .tables import (RDTB, RDCTB, GCTB, CHTB, KYTB, MRFTB, WRTB, CROPROTATION)