"""SWAP model package

The main subpackage for the SWAP model.

Modules:
    model: Building, running and parsing the results of a SWAP model run.
    result: Capturing model results.
    metadata: Model metadata.
"""

from pyswap.model.metadata import Metadata
from pyswap.model.model import Model
from pyswap.model.result import Result

__all__ = [
    "Metadata",
    "Model",
    "Result",
]
