from dataclasses import dataclass, field
from pyswap.core.utils.dtypes import Subsection


@dataclass
class Metadata(Subsection):
    """Metadata of a SWAP model. 

    When model with the same metedata object is saved multiple times in the database, it's always considered as "model version".
    """

    author: str
    institution: str
    email: str
    project_name: str
    swap_ver: str
    comment: str | None = None
