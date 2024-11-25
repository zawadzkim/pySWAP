"""
# SWAP model package

The main subpackage for the SWAP model.

Modules:
    model: SWAP model settings.
    result: SWAP model result.
    metadata: SWAP model metadata.
"""

from pyswap.model.metadata import Metadata
from pyswap.model.model import Model
from pyswap.model.result import Result

__all__ = [
    "Metadata",
    "Model",
    "Result",
]
