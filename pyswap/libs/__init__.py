from importlib import resources
from importlib.abc import Traversable
import yaml
from pathlib import Path

all_paths: Traversable = resources.files(__name__)
"""The whole directory of test groundwater sensor data."""

crop_params: Traversable = all_paths / "WOFOST_crop_parameters"
"""The directory of WOFOST crop parameters."""

RULES_FILE = all_paths / "validation.yaml"
"""The path to the validation rules file."""

def load_validation_rules():
    """Load validation rules from the YAML file."""
    with open(RULES_FILE, "r") as file:
        return yaml.safe_load(file)

VALIDATIONRULES = load_validation_rules()