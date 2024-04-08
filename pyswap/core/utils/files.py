import chardet


def open_file(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    encoding = chardet.detect(raw_data)['encoding']
    return raw_data.decode(encoding)


def save_file(string: str,
              fname: str,
              path: str,
              mode: str,
              extension: str | None = None,
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
    if extension is not None:
        fname = f'{fname}.{extension}'

    with open(f'{path}/{fname}', f'{mode}', encoding=f'{encoding}') as f:
        f.write(string)
