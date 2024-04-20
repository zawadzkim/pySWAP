"""
Module for quick check of the current OS and getting the base path.

Functions:
    is_windows: Checks if the current OS is Windows.
    get_base_path: Returns properly formatted current directory path depending on OS.
"""

import platform


def is_windows() -> bool:
    """Checks if the current OS is Windows."""
    return True if platform.system() == 'Windows' else False


def get_base_path() -> str:
    """Returns properly formatted current directory path depending on OS."""
    return '.\\' if is_windows() else './'
