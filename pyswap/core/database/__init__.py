"""
All modules related to the database connection and models.


!!! warning
    This module is in review and may be significantly changed or removed in the future.

!!! tip
    pySWAP is meant to enable saving model runs to a SQLite database. That way, the users will be 
    able to easily exchange models they built and run them on their own machines.
"""
from .hdf5 import HDF5
