"""
# Simulation settings

Main simulation settings for the SWAP model.

Modules:
    general: General simulation settings for the SWAP model.
    metadata: Metadata for the SWAP model.
    richards: Richards simulation settings for the SWAP model.
"""
from .metadata import Metadata
from .general import GeneralSettings
from .richards import RichardsSettings
from .location import Location, MeteoLocation, ModelLocation
