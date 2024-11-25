import chardet


def open_file(file_path: str) -> str:
    """Open file and detect encoding.

    Arguments:
        file_path (str): Path to the file to be opened.
    """
    with open(file_path, "rb") as f:
        raw_data = f.read()
    encoding = chardet.detect(raw_data)["encoding"]

    return raw_data.decode(encoding)