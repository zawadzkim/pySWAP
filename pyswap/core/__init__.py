"""
# Core subpackage

Core package containing the main classes and functions for the SWAP model.

Modules:
    basemodel: Base model class for pySWAP.
    fields: Field types for pyswap used for serialization.
    files: Functions to interact with file system.
    serializers: Functions to fine tune the serializatino of pySWAP objects.
    valueranges: Objects containing value ranges used is validation of
        pySWAP objects.
___________________________________________________________________________
"""

from .mixins import FileMixin, SerializableMixin, ComplexSerializableMixin
from .basemodel import PySWAPBaseModel
from .fields import (Table, Arrays, CSVTable, DayMonth, IntList,
                     StringList, FloatList, DateList, Switch,
                     ObjectList, String)
from .files import open_file, save_file
from .serializers import (serialize_table, serialize_arrays,
                          serialize_csv_table,
                          serialize_object_list)
from .valueranges import UNITRANGE, YEARRANGE, DVSRANGE
from .tablevalidation import BaseTableModel
