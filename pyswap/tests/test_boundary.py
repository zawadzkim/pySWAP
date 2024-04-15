import pytest
from pyswap.core.boundary import LateralDrainage
from pydantic import ValidationError


def test_lateral_drainage_swdra_gt1_lte2_no_drfil():
    with pytest.raises(ValidationError, match='drfil must be provided if swdra is 1 or 2'):
        LateralDrainage(swdra=1, drfil=None)
    with pytest.raises(ValidationError, match='drfil must be provided if swdra is 1 or 2'):
        LateralDrainage(swdra=2)


def test_lateral_drainage_swdra_gt_2():
    with pytest.raises(ValueError):
        LateralDrainage(swdra=3)
