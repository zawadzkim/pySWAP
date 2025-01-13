"""Variables shared across the package.

Variables:
    IS_WINDOWS: Whether the system is Windows.
    BASE_PATH: Representation of file path depending on the system.
    root: Root directory of the package.
    validation_rules: Path to YAML validation rules.
    VALIDATIONRULES: Validation rules for the package as dictionary.
"""

from importlib import resources
from importlib.abc import Traversable
import platform
from pyswap.core.io.io_yaml import load_yaml


IS_WINDOWS = platform.system() == "Windows"
"""Whether the system is Windows."""

BASE_PATH = ".\\" if IS_WINDOWS else "./"
"""Representation of file path depending on the system."""

root: Traversable = resources.files("pyswap")
"""Root directory of the package."""

validation_rules: Traversable = root / "core" / "validation.yaml"
VALIDATIONRULES = load_yaml(validation_rules)
