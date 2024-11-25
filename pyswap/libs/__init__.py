from importlib import resources
from importlib.abc import Traversable

libs: Traversable = resources.files(__name__)
"""Libs module directory."""

swap_linux: Traversable = libs / "swap420-linux" / "swap420"
"""The directory of the SWAP420 Linux executable."""

swap_windows: Traversable = libs / "swap420-exe" / "swap420.exe"
"""The directory of the SWAP420 Windows executable."""

crop_params: Traversable = libs / "WOFOST_crop_parameters"
"""The directory of WOFOST crop parameters."""
