"""Classes that wrap the crop parameters database for WOFOST (A. de Wit).

From the classes here, only the WOFOSTCropDB is directly accessed by the user,
however, the final usable object will be the CropVariety.

Classes:
    WOFOSTCropFile: Manage a single WOFOST crop file content.
    CropVariety: Manage crop variety parameters.
    WOFOSTCropDB: Manage a single WOFOST crop file content.
"""

from pathlib import Path
from pprint import pprint

from pydantic import BaseModel, computed_field

from pyswap.core.io.io_yaml import load_yaml
from pyswap.libs import crop_params


class WOFOSTCropFile(BaseModel):
    """Manage a single WOFOST crop file content.

    Attributes:
        yaml_content: The entire content of the YAML file.

    Properties:
        metadata: Metadata of the crop file.
        ecotypes: List of eco-types.
        genericc3: Generic settings for C3 crop types.
        genericc4: Generic settings for C4 crop types.
        varieties: List of available varieties.

    Methods:
        get_variety: Get the parameters of a specific variety.
    """

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
        return CropVariety(
            variety=self.yaml_content["CropParameters"]["Varieties"][variety]
        )


class CropVariety(BaseModel):
    """Manage crop variety parameters.

    Attributes:
        variety: Parameters for crop variety from the YAML file (with metadata).

    Properties:
        parameters: Bare parameters of the variety (all metadata removed).
        metadata: The metadata of the variety.
    """

    variety: dict

    @computed_field(return_type=dict)
    def parameters(self):
        params = {
            k.lower(): v[0]
            for k, v in self.variety.items()
            if k != "Metadata" and v[0] != -99.0
        }
        return self._format_tables(params)

    @computed_field(return_type=dict)
    def metadata(self):
        return self.variety["Metadata"]

    @staticmethod
    def _format_tables(table: dict) -> dict[str, list[list]]:
        """pre-format tables from YAML to a list of lists.

        In the YAML file, the tables are seem to be formatted
        in a way where the odd elements in the lists are one
        column and the even elements are the other. This method
        converts this format to a dictionary with two lists.
        """

        formatted = {
            k: [list(row) for row in zip(v[::2], v[1::2], strict=False)]
            if isinstance(v, list)
            else v
            for k, v in table.items()
        }

        return formatted


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

    def load_crop_file(self, crop: str) -> WOFOSTCropFile:
        """Load a specific crop file and return the content as a dictionary"""
        path = (
            self.libdir / f"{crop}"
            if crop.endswith(".yaml")
            else self.libdir / f"{crop}.yaml"
        )
        return WOFOSTCropFile(yaml_content=load_yaml(path))


__all__ = ["WOFOSTCropDB"]
