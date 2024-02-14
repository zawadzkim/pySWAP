from dataclasses import dataclass, field


@dataclass
class Metadata:
    """Metadata of a SWAP model. Always has to be attached to a SWAP model object"""
    author: str
    institution: str
    email: str
    project_name: str
    swap_ver: str
    comment: str = field(default='No comment')
