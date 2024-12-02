"""Script reading YAML crop settings files."""


# %%
import os
from pathlib import Path
from pprint import pprint
from pyswap.libs import crop_params
from pyswap.core.io.io_yaml import load_yaml
from pydantic import BaseModel, computed_field

class WOFOSTCropFile(BaseModel):
    """Class for managing the content of a single WOFOST crop parameters file"""

    yaml_content: dict

    @computed_field(return_type=dict)
    def metadata(self):
        return self.yaml_content["Metadata"]

    @computed_field(return_type=dict)
    def ecotypes(self):
        return list(self.yaml_content["CropParameters"]["EcoTypes"])

    @computed_field(return_type=dict)
    def genericc3(self):
        """Get generic settings for C3 crop types - plants that bind CO2 into
        3-phosphoglycerate having three carbon atoms. E.g., wheat, rice"""
        return self.yaml_content["CropParameters"]["GenericC3"]

    @computed_field(return_type=dict)
    def genericc4(self):
        """Get generic settings for C4 crop types - plants that bind CO2 into
        oxaloacetate having four carbon atoms. E.g., maize, sugarcane"""
        return self.yaml_content["CropParameters"]["GenericC4"]

    @computed_field(return_type=dict)
    def varieties(self):
        return list(self.yaml_content["CropParameters"]["Varieties"])

    @staticmethod
    def _serialize_variety(variety_dict: dict, what: str):
        variety_dict.pop("Metadata")
        if what == "parameters":
            return {k: v[0] for k, v in variety_dict.items()}
        if what == "explanation":
            return {k: f"{v[1]} {v[2]}" for k, v in variety_dict.items()}

    def get_variety(self, variety: str, what: str = "parameters"):
        content = self.yaml_content["CropParameters"]["Varieties"][variety]
        return self._serialize_variety(content, what=what)

    def get_variety_meta(self, variety: str):
        content = self.yaml_content["CropParameters"]["Varieties"][variety]
        return content["Metadata"]

    def populate_attributes(self, params: dict):
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Attribute '{key}' does not exist in the class.")

class WOFOSTCropDB(BaseModel):
    """Simple class for managing crop parameters files.

    Initially, it's meant to be used with A. de Wit's WOFOST crop parameters
    database which is a collection of YAML files. However, it can be easily
    extended to support other formats and databases when they emerge. All
    methods should return the content as WOFOSTCropFile instances. This way
    we ensure that whatever the source format is, the content is always
    usable in the same way.

    Attributes:
        libdir: Path to the directory with crop parameters

    Properties:
        croptypes: List all available crop types (files in the directory)
    
    Methods:
        load_crop_file: Load a specific crop file and return the content as a
            WOFOSTCropFile instance
    """

    libdir: Path = crop_params

    @computed_field(return_type=None)
    def croptypes(self):
        """Print the list of available files"""
        pprint(load_yaml(crop_params / "crops.yaml")["available_crops"])


    @staticmethod
    def format_tables(table: list) -> dict:
        """Format tables from YAML to a dictionary with two lists.
        
        In the YAML file, the tables seem to be formatted
        in a way where the odd elements in the lists are one
        column and the even elements are the other. This method
        converts this format to a dictionary with two lists.
        """
        return {
            "col1": table[::2],
            "col2": table[1::2]
        }
    
    def load_crop_file(self, crop: str):
        """Load a specific crop file and return the content as a dictionary"""
        path = self.libdir / f"{crop}" if crop.endswith(".yaml") else self.libdir / f"{crop}.yaml"
        return WOFOSTCropFile(yaml_content=load_yaml(path))



# %%
db = WOFOSTCropDB()
db.croptypes

# %%

potato = db.load_crop_file("potato")
potato.varieties

# %%

potato_params = potato.get_variety("Potato_701")

# %%
import pandas as pd

VERNRTB = potato_params["VERNRTB"]

df = pd.DataFrame(db.format_tables(VERNRTB))

df

# %%

# Example usage:
potato = db.load_crop_file("potato")
params = {
    'CO2EFFTB': [40.0, 0.0, 360.0, 1.0, 720.0, 1.11, 1000.0, 1.11, 2000.0, 1.11],
    'NON_EXISTENT_ATTR': 123,  # This will trigger a warning
    # ... other parameters ...
}
potato.populate_attributes(params)


# %%
from typing import get_origin, get_args
from typing_extensions import Annotated, Union

def is_annotated_table_or_array(attr_type):
    origin = get_origin(attr_type)
    if origin is Annotated:
        base_type = get_args(attr_type)[-1]
        return base_type in ["Table", "Arrays", "ObjectList"]
    elif origin is Union:
        return any(is_annotated_table_or_array(arg) for arg in get_args(attr_type))
    return False

def check_attributes(cls):
    for attr_type in cls.__annotations__.values():
        return is_annotated_table_or_array(attr_type)


from pyswap import CropDevelopmentSettingsFixed

print(check_attributes(CropDevelopmentSettingsFixed))
# %%
