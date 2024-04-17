from .hupsel import _run_hupsel
from typing import Literal


def run_testcase(case: Literal['hupsel']):
    if case == 'hupsel':
        result = _run_hupsel()
    else:
        raise ValueError(f'provided case ({case}) is not available.')

    return result
