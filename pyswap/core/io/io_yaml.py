"""Interact with YAML files.

Functions:
    load_yaml: Load a YAML file.
"""

from pathlib import Path

import yaml


def load_yaml(file: Path) -> dict:
    """Load a YAML file.

    Arguments:
        file: Path to the YAML file.
    """
    with open(file) as file:
        content: dict = yaml.safe_load(file)

    return content
