"""
# Irrigation subpackage

Irrigation settings for the SWAP simulation.

Modules:
    irrigation: The irrigation settings.
    irgfile: The irrigation file.
"""

from .irgfile import IrgFile
from .irrigation import FixedIrrigation, ScheduledIrrigation
from .tables import IRRIGATION
