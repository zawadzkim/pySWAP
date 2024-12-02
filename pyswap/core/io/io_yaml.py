"""Interact with YAML files."""

import yaml


def load_yaml(file) -> dict:
    """Load a YAML file.

    Arguments:
        file: Path to the YAML file.
    """
    with open(file) as file:
        return yaml.safe_load(file)
