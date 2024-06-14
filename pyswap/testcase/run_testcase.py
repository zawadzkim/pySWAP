from .hupselbrook import _make_hupselbrook
from typing import Literal


def get(case: Literal['hupselbrook']):
    if case == 'hupselbrook':
        model = _make_hupselbrook()
    else:
        raise ValueError(f'provided case ({case}) is not available.')

    return model
