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


def list_to_string(dates: list,
                   newline: bool = True,
                   separator: str = '') -> str:
    """
    Converts a list into a string.

    Args:
        dates: A list to be converted into a string.
        newline: Whether the items in the list should be separated by newline characters (True) or commas (False).
        separator: The separator to use if newline is False.

    Returns:
        A string containing the items from the list.

    Raises:
        TypeError: If dates is not a list.
    """

    if newline is True:
        string_of_dates: str = ''.join([str(date) + '\n' for date in dates])
    else:
        string_of_dates: str = separator.join([str(date) for date in dates])

    return string_of_dates


def check_required_kwargs(required_kwargs: list, keys: list):
    """
    Check if all required kwargs are given to the function allowing kwargs.

    :param list required_kwargs: list of required kwargs defined in the function
    :param list keys: list of kwargs passed to the function, should be constructed from **kwargs in the function.
    """
    if all(key in keys for key in required_kwargs):
        pass
    else:
        raise KeyError(f'not all required arguments are given. \n '
                       f'Missing arguments: {list(set(required_kwargs) - set(keys))}')


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

    with open(f'{path}/{fname}.{extension}', f'{mode}', encoding=f'{encoding}') as file:
        file.write(string)


def set_cwd() -> None:
    """
       Sets the current working directory to the directory of the script that called this function.

       Args:
           None.

       Returns:
           None.

       Raises:
           Any exceptions raised by the chdir() function.
       """
    from os import chdir
    from os.path import abspath, dirname
    abspath = abspath(__file__)
    dname = dirname(abspath)
    chdir(dname)
    print(f'Current working environment set to: {dname}')


