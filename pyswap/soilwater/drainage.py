import os
from dataclasses import dataclass, field
from ..base.utils import open_file


@dataclass
class Drainage:

    file_path: str
    file_name: str = field(default=None)
    file_extension: str = field(default=None)
    file: dict = field(default_factory=dict)

    def __post_init__(self):
        self.file_name, self.file_extension = os.path.splitext(
            os.path.basename(self.file_path))
        self.file[self.file_name] = open_file(self.file_path, encoding='ascii')
