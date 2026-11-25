"""Interact with ASCII files.

Functions:
    open_ascii: Open a SWAP text file (UTF-8, falling back to Latin-1).
    save_ascii: Save a string to an ASCII file.
"""

from pathlib import Path


def open_ascii(file_path: Path) -> str:
    """Open a SWAP text file and return its content.

    SWAP input and output files are plain ASCII, except for a few characters
    in comments and headers written by SWAP or Windows editors in Latin-1
    (e.g. the degree sign in "ºC" in the .vap output). The file is decoded as
    UTF-8 (which covers ASCII) and, if that fails, as Latin-1, which accepts
    any byte. This replaces encoding detection with chardet and gives the same
    text for the bundled inputs and SWAP outputs.

    Arguments:
        file_path (str): Path to the file to be opened.
    """
    raw_data = Path(file_path).read_bytes()
    try:
        return raw_data.decode("utf-8")
    except UnicodeDecodeError:
        return raw_data.decode("latin-1")


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
