from dataclasses import dataclass, field
from ..base.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class LateralDrainage(Subsection):
    """Lateral drainage to surface water."""

    swdra: int
    drfil: str | None = None

    def __post_init__(self):
        if self.swdra not in range(0, 3):
            raise ValueError('swdra must be 0, 1, or 2')

        if self.swdra in range(1, 3):
            assert self.drfil, 'drfil must be provided if swdra is 1 or 2'


@dataclass
class BottomBoundary(Subsection):

    swbbcfile: bool
    swbotb: int
    bbcfile: str | None = None
    # if swbotb == 1
    gwlevel: DataFrame | None = None
    # if swbotb == 2
    sw2: int | None = None
    # if sw2 == 1
    sinave: float | None = None
    sinamp: float | None = None
    sinmax: float | None = None
    # if sw2 == 2
    qbot: DataFrame | None = None
    # if swbotb == 3
    swbotb3resvert: int | None = None
    swbotb3impl: int | None = None
    shape: float | None = None
    hdrain: float | None = None
    rimlay: float | None = None
    sw3: int | None = None
    # if sw3 == 1
    aquave: float | None = None
    aquamp: float | None = None
    aqtmax: float | None = None
    aqtper: float | None = None
    # if sw3 == 2
    haquif: DataFrame | None = None
    sw4: int | None = None
    # if sw4 == 1
    qbot4: DataFrame | None = None
    # if swbotb == 4
    swqhbot: int | None = None
    # if swqhbot == 1
    cofqha: float | None = None
    cofqhb: float | None = None
    cofqhc: float | None = None  # optional
    # if swqhbot == 2
    qtab: DataFrame | None = None
    # if swbotb == 5
    hbot5: DataFrame | None = None

    def __post_init__(self):
        if self.swbotb not in range(1, 9):
            raise ValueError('swbotb must be 1 to 8')

        if self.swbbcfile:
            assert self.gwlevel is not None, 'gwlevel must be provided if swbbcfile is True'
