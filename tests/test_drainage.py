import pytest
from pydantic import ValidationError

from pyswap.components.drainage import DraFile


def test_swdivd_accepts_swap_values():
    # SWAP reads SWDIVD as 0 (no vertical distribution) or 1 (distribute).
    assert DraFile(dramet=3, swdivd=0).swdivd == 0
    assert DraFile(dramet=3, swdivd=1, cofani=[1.0]).swdivd == 1


def test_swdivd_rejects_two():
    with pytest.raises(ValidationError, match="swdivd"):
        DraFile(dramet=3, swdivd=2)

