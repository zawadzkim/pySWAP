"""Variables shared across the package.

Variables:
    IS_WINDOWS: Whether the system is Windows.
    BASE_PATH: Representation of file path depending on the system.
    root: Root directory of the package.
    validation_rules: Path to YAML validation rules.
    VALIDATIONRULES: Validation rules for the package as dictionary.
"""

import platform
from importlib import resources
from pathlib import Path

from pyswap.core.io.io_yaml import load_yaml

IS_WINDOWS = platform.system() == "Windows"
"""Whether the system is Windows."""

BASE_PATH = ".\\" if IS_WINDOWS else "./"
"""Representation of file path depending on the system."""

root: Path = resources.files("pyswap")
"""Root directory of the package."""

validation_rules: Path = root / "core" / "validation.yaml"
VALIDATIONRULES = load_yaml(validation_rules)

FNAME_IN: str = "swap"
"""Generic name for the SWAP input files."""

FNAME_OUT: str = "result"
"""Generic name for the SWAP output files."""

ADDITIONAL_SWITCHES: list[str] = [
    "schedule",
    "isuas",
    "tcs",
    "tcsfix",
    "dcs",
    "dcslim",
    "dramet",
    "ipos",
    "idev",
    "idsl",
]

EXTENSIONS: list[str] = [
    "wba",
    "end",
    "vap",
    "bal",
    "blc",
    "sba",
    "ate",
    "bma",
    "drf",
    "swb",
    "ini",
    "inc",
    "crp",
    "str",
    "irg",
    "csv",
    "csv_tz",
]

EXTENSION_SWITCHES: list[str] = [f"sw{ext}" for ext in EXTENSIONS]
