"""
# Irrigation subpackage

Irrigation settings for the SWAP simulation.

Modules:
    irrigation: The irrigation settings.
    irgfile: The irrigation file.
"""

from .irrigation import ScheduledIrrigation, FixedIrrigation
from .irgfile import IrgFile
from .tables import IRRIGATION
