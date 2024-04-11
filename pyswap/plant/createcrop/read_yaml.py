"""Script reading YAML crop settings files."""
import os
from pathlib import Path
from typing import Optional
import yaml
from pprint import pprint
from pydantic import BaseModel, computed_field

LIBDIR: Path = Path('pyswap/libs/WOFOST_crop_parameters').absolute()


def croptypes():
    """Print the list of available files"""
    pprint([file for file in os.listdir(LIBDIR)
            if file.endswith('.yaml')])


def read_yaml(fname: str, path: Optional[str] = None) -> str:
    def read(path: str) -> str:
        with path.open('r') as f:
            content = yaml.safe_load(f)
            return content
    if not path:
        return WOFOSTCrop(
            yaml_content=read(Path(LIBDIR, fname).with_suffix('.yaml').absolute()))
    else:
        return WOFOSTCrop(
            yaml_content=read(Path(path, fname).with_suffix('.yaml').absolute()))


class WOFOSTCrop(BaseModel):
    """Class for managing the library of WOFOST crop parameters from https://github.com/ajwdewit.

    The library is included as a submodule in pySWAP and is located at pyswap/libs/WOFOST_crop_parameters.
    All files in that library have .yaml extension and fairly uniform format so it made sense to set up a 
    pySWAP specific data structure for reading them.
    """
    libdir: Path = LIBDIR
    yaml_content: dict

    @computed_field(return_type=dict)
    def metadata(self):
        return self.yaml_content['Metadata']

    @computed_field(return_type=dict)
    def ecotypes(self):
        return list(self.yaml_content['CropParameters']['EcoTypes'])

    @computed_field(return_type=dict)
    def genericc3(self):
        """Get generic settings for C3 crop types - plants that bind CO2 into 
        3-phosphoglycerate having three carbon atoms. E.g., wheat, rice"""
        return self.yaml_content['CropParameters']['GenericC3']

    @computed_field(return_type=dict)
    def genericc4(self):
        """Get generic settings for C4 crop types - plants that bind CO2 into 
        oxaloacetate having four carbon atoms. E.g., maize, sugarcane"""
        return self.yaml_content['CropParameters']['GenericC4']

    @computed_field(return_type=dict)
    def varieties(self):
        return list(self.yaml_content['CropParameters']['Varieties'])

    @staticmethod
    def _serialize_variety(variety_dict: dict, what: str):
        variety_dict.pop("Metadata")
        if what == "parameters":
            return {k: v[0] for k, v in variety_dict.items()}
        if what == "explanation":
            return {k: f'{v[1]} {v[2]}' for k, v in variety_dict.items()}

    def get_variety(self, variety: str, what: str = 'parameters'):
        content = self.yaml_content['CropParameters']['Varieties'][variety]
        return self._serialize_variety(content, what=what)

    def get_variety_meta(self, variety: str):
        content = self.yaml_content['CropParameters']['Varieties'][variety]
        return content['Metadata']


if __name__ == '__main__':
    wmaize = read_yaml('maize')
    string = ''
    for k, v in wmaize.get_variety('Grain_maize_201').items():
        string += f'{k} = {v}\n'
    print(string)
