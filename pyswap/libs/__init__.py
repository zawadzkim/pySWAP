"""External resources for SWAP model and SWAP 4.2 executables.

This module contains the paths to the SWAP model and SWAP 4.2 executables and
external resources, allowing for easy access to them throughout the package. The
following resources are available:

Modules:
    libs: The root directory of the `libs` module.
    swap_linux: The directory of the SWAP420 Linux executable.
    swap_windows: The directory of the SWAP420 Windows executable.
    crop_params: The directory of WOFOST crop parameters.

Linux and Windows executables are compiled executables distributed with the
SWAP 4.2 model through the main website of the SWAP model
(https://www.swap.alterra.nl/). The license of the source code provided with the
precompiled executables is included in the `libs` root.

The WOFOST crop parameters shipped with the package as submodule come from
GitHub repository of Allard de Wit
(https://github.com/ajwdewit/WOFOST_crop_parameters)
"""

from importlib import resources
from importlib.abc import Traversable

libs: Traversable = resources.files(__name__)
"""Libs module directory."""

swap_linux: Traversable = libs / "swap420-linux" / "swap420"
"""The directory of the SWAP420 Linux executable."""

swap_windows: Traversable = libs / "swap420-exe" / "swap.exe"
"""The directory of the SWAP420 Windows executable."""

crop_params: Traversable = libs / "WOFOST_crop_parameters"
"""The directory of WOFOST crop parameters."""

plotting: Traversable = libs / "plotting"
"""The directory of plotting resources."""
