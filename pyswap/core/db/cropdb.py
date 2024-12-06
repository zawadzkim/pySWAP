"""
# Crop database

This module wraps the crop parameters database for WOFOST (A. de Wit).

!!! warning
    This module is a part of a broader effort to integrate the WOFOST
    crop parameter database into pySWAP. There WILL be some refactoring
    in the near future.
"""

from pathlib import Path
from pprint import pprint
from pyswap.libs import crop_params
from pyswap.core.io.io_yaml import load_yaml
from pydantic import BaseModel, computed_field
import pandera as pa

from typing import Literal


class WOFOSTCropFile(BaseModel):
    """Class for managing the content of a single WOFOST crop parameters file"""

    yaml_content: dict

    @computed_field(return_type=dict)
    def metadata(self):
        """Metadata of the yaml crop file"""
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

    def get_variety(self, variety: str):
        return CropVariety(variety=self.yaml_content["CropParameters"]["Varieties"][variety])

class CropVariety(BaseModel):
    """Wrapping the variety in a separate class to make it easier to access.
    
    Attributes:
        variety: The entire variety dictionary from the YAML file (incl. metadata).

    Properties:
        parameters: Bare parameters of the variety (all metadata removed).
        metadata: The metadata of the variety.
    """
    variety: dict

    @computed_field(return_type=dict)
    def parameters(self):
        return {k: v[0] for k, v in self.variety.items() if k != "Metadata" and v[0] != -99.0}
    
    @computed_field(return_type=dict)
    def metadata(self):
        return self.variety["Metadata"]
    
    @staticmethod
    def get_table_class(class_name: str):
        """Get the schema class of a table.
        
        In pySWAP tables are validated with Pandera DataFrameModel. Each table
        required by SWAP has its own schema class. This method returns the
        schema class of a table based on its name.

        Parameters:
            class_name: Name of the table class. Meant to be automatically
                generated from the key in the YAML file.

        Returns:
            class_: The schema class of the table if it exists, otherwise None.
        """
        import importlib
        module = importlib.import_module("pyswap.components.crop")
        if hasattr(module, class_name):
            class_ = getattr(module, class_name)
            return class_ if issubclass(class_, pa.DataFrameModel) else None
        else:
             None
    
    def format_tables(self):
        variety = self.parameters
        for k, v in variety.items():
            table_class = self.get_table_class(k)
            if table_class:
                cols = list(table_class.__annotations__.keys())
                if isinstance(v, list):
                    variety[k] = table_class.create(self._format_tables(v), columns=cols)
        return variety
    
    @staticmethod
    def _format_tables(table: list) -> dict:
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
        
    def load_crop_file(self, crop: str):
        """Load a specific crop file and return the content as a dictionary"""
        path = self.libdir / f"{crop}" if crop.endswith(".yaml") else self.libdir / f"{crop}.yaml"
        return WOFOSTCropFile(yaml_content=load_yaml(path))


__all__ = ["WOFOSTCropDB"]