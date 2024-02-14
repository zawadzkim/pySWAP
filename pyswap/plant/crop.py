from dataclasses import dataclass, field
from typing import Any
from ..base.utils import open_file
from ..base.dtypes import Section, Table
from pandas import DataFrame


@dataclass
class CropData:

    file_names: list
    file_paths: list
    files: dict = field(default_factory=dict)

    def __post_init__(self):
        for file_name, file_path in zip(self.file_names, self.file_paths):
            self.files[file_name] = open_file(file_path, encoding='ascii')


@dataclass
class Crop(Section):
    """Holds the crop settings of the simulation."""

    swcrop: bool
    rds: float = None,
    croprotation: dict[list] | DataFrame = None,

    def __post_init__(self):
        if self.swcrop:
            assert self.rds is not None, "rds must be specified if swcrop is True"
            assert self.croprotation is not None, "croprotation must be specified if swcrop is True"

    def __setattr__(self, name, value) -> None:
        if name == "croprotation" and value is not None:
            assert isinstance(value, dict) or isinstance(
                value, DataFrame), "croprotation must be an instance of dict or DataFrame"
            if isinstance(value, dict):
                value = Table(value)
        super().__setattr__(name, value)
