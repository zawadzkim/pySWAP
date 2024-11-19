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

from .basemodel import PySWAPBaseModel
from .fields import (
    Arrays,
    CSVTable,
    DateList,
    DayMonth,
    FloatList,
    IntList,
    ObjectList,
    String,
    StringList,
    Switch,
    Table,
)
from .files import open_file, save_file
from .mixins import ComplexSerializableMixin, FileMixin, SerializableMixin
from .serializers import (
    serialize_arrays,
    serialize_csv_table,
    serialize_object_list,
    serialize_table,
)
from .tablevalidation import BaseTableModel
from .valueranges import DVSRANGE, UNITRANGE, YEARRANGE
