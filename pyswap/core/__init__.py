"""
## Core subpackage

Core package containing the main classes and functions for the SWAP model. It is used only internally
by the package. None of the functionality is exposed to the user.

Modules:
    basemodel: Base model class for pySWAP.
    fields: Field types for pyswap used for serialization.
    files: Functions to interact with file system.
    serializers: Functions to fine tune the serializatino of pySWAP objects.
    valueranges: Objects containing value ranges used is validation of
        pySWAP objects.
"""

import platform
from importlib import resources
from importlib.abc import Traversable

from pyswap.core.io.yaml import load_yaml

root: Traversable = resources.files("pyswap")
"""Root directory of the package."""

validation_rules: Traversable = root / "core" / "validation.yaml"

VALIDATIONRULES = load_yaml(validation_rules)

IS_WINDOWS = platform.system() == "Windows"
BASE_PATH = ".\\" if IS_WINDOWS else "./"

