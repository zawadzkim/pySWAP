"""Database integrations for pySWAP.

This module contains classes and functions that allow pySWAP to interact with
databases. Currently, there is support for the WOFOST crop database (with the
WOFOSTCropDB class) and the HDF5 file format (with the HDF5 class).

### HDF5
Thanks to the HDF5 integration, users will be able to save their models and
results to a single .h5 file. HDF5 databases are binary files that can store
large amounts of data in a structured way. This format is widely used in the
scientific community and is supported by many programming languages and
different platforms. The idea is that

### WOFOST crop database
The WOFOST crop database is a database containing crop parameters for the
WOFOST model in files in YAML format. The WOFOSTCropDB class allows users to
load a particular variaty of a crop with the corresponding parameters and update
the pySWAP models with them.

Modules:
    hdf5: Class for interacting with HDF5 files.
    cropdb: Classes that wrap the crop parameters database for
        WOFOST (A. de Wit).
"""

from pyswap.db.cropdb import CropVariety, WOFOSTCropDB
from pyswap.db.hdf5 import HDF5

__all__ = ["HDF5", "CropVariety", "SoilProfile", "SoilProfilesDB", "WOFOSTCropDB"]
