# %%
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

# %%


class CropYAML(BaseModel):
    version: str
    metadata: dict
    cropparameters: dict


def read_yaml(path: Path):
    with open(path) as file:
        return yaml.safe_load(file)


def get_varieties(crop_yaml: dict):
    return crop_yaml["CropParameters"]["Varieties"]


# %%
def get_parameters(variety: dict):
    return {parameter: value[0] for parameter, value in variety.items()}


# %%


def generate_dvs_list(
    array: list,
    dvs_start: float,
    dvs_end: float,
    method: Literal["linear", "logarithmic", "exponential"] = "linear",
):
    """Generate a list of evenly spaced DVS values"""

    if method == "linear":
        return [
            dvs_start + (dvs_end - dvs_start) / (len(array) - 1) * i
            for i in range(len(array))
        ]
    elif method == "logarithmic":
        # generate the list of dvs not evenly spaced (logarithmic)
        dvs = [
            dvs_start + (dvs_end - dvs_start) / (len(array) - 1) * i
            for i in range(len(array))
        ]
        # convert the list to a logarithmic scale
        return [10 ** dvs[i] for i in range(len(dvs))]
    elif method == "exponential":
        # generate the list of dvs not evenly spaced (exponential)
        dvs = [
            dvs_start + (dvs_end - dvs_start) / (len(array) - 1) * i
            for i in range(len(array))
        ]
        # convert the list to an exponential scale
        return [2 ** dvs[i] for i in range(len(dvs))]
    else:
        raise ValueError(
            "Method must be either 'linear', 'logarithmic' or 'exponential'"
        )

# %%
from pyswap.libs import crop_params

path_potato = crop_params / "potato.yaml"
potato_yaml = read_yaml(path_potato)

potato_varieties = get_varieties(potato_yaml)

# %%
