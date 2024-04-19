import platform


def is_windows() -> bool:
    return True if platform.system() == 'Windows' else False


def get_base_path() -> str:
    return '.\\' if is_windows() else './'
