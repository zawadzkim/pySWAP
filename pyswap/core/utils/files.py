def open_file(file_path: str,
              encoding: str) -> str:
    """
    Opens, reads and closes a file.

    Args:
        file_path: The path to the file to be opened.
        encoding: encoding while opening.


    Raises:
        Any exceptions raised by the open() or read() functions.
    """

    with open(str(file_path), encoding=encoding, mode='r') as fhandle:
        string = fhandle.read()

    return string


def save_file(string: str,
              extension: str,
              fname: str,
              path: str,
              mode: str,
              encoding: str = 'ascii'):
    """
    Saves a string to a file.

    Args:
        string: The string to be saved to a file.
        extension: The extension that the file should have (e.g. 'txt', 'csv', etc.).
        fname: The name of the file.
        path: The path where the file should be saved.
        mode: The mode in which the file should be opened (e.g. 'w' for write, 'a' for append, etc.).
        encoding: The encoding to use for the file (default is 'ascii').

    Returns:
        None.

    Raises:
        Any exceptions raised by the open() or write() functions.
    """

    with open(f'{path}/{fname}.{extension}', f'{mode}', encoding=f'{encoding}') as f:
        f.write(string)
