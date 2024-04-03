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
