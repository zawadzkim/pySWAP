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
from pathlib import Path

libs: Path = resources.files(__name__)
"""Libs module directory."""

swap: Path = libs / "swap"
"""The directory of the SWAP executable."""

swap_linux: Path = swap / "swap420"
"""The directory of the SWAP420 Linux executable."""

swap_windows: Path = swap / "swap.exe"
"""The directory of the SWAP420 Windows executable."""

crop_params: Path = libs / "WOFOST_crop_parameters"
"""The directory of WOFOST crop parameters."""

plotting: Path = libs / "plotting"
"""The directory of plotting resources."""

co2concentration: Path = libs / "co2-concentration" / "Atmospheric.co2"
