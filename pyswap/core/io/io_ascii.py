"""Interact with ASCII files.

Functions:
    open_ascii: Open an ASCII file and detect its encoding.
    save_ascii: Save a string to an ASCII file.
"""

from pathlib import Path

import chardet


def open_ascii(file_path: Path) -> str:
    """Open file and detect encoding.

    Arguments:
        file_path (str): Path to the file to be opened.
    """
    with open(file_path, "rb") as f:
        raw_data = f.read()
    encoding = chardet.detect(raw_data)["encoding"]

    return raw_data.decode(encoding)


def save_ascii(
    string: str,
    fname: str,
    path: str,
    mode: str = "w",
    extension: str | None = None,
    encoding: str = "ascii",
) -> None:
    """
    Saves a string to a file with a given extension.

    Parameters:
        string (str): The string to be saved to a file.
        extension (str): The extension that the file should have (e.g. 'txt', 'csv', etc.).
        fname (str): The name of the file.
        path (str): The path where the file should be saved.
        mode (str): The mode in which the file should be opened (e.g. 'w' for write, 'a' for append, etc.).
        encoding (str): The encoding to use for the file (default is 'ascii').

    Returns:
        None
    """

    if extension is not None:
        fname = f"{fname}.{extension}"

    with open(f"{path}/{fname}", f"{mode}", encoding=f"{encoding}") as f:
        f.write(string)
