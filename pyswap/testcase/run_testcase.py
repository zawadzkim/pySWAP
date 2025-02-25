from typing import Literal

from .grassgrowth import _make_grassgrowth
from .hupselbrook import _make_hupselbrook
from .macroporeflow import _make_macroporeflow
from .oxygenstress import _make_oxygenstress
from .salinitystress import _make_salinitystress
from .surfacewater import _make_surfacewater


def get(
    case: Literal[
        "hupselbrook",
        "oxygenstress",
        "grassgrowth",
        "macroporeflow",
        "salinitystress",
        "surfacewater",
    ],
):
    cases = {
        "hupselbrook": _make_hupselbrook,
        "oxygenstress": _make_oxygenstress,
        "grassgrowth": _make_grassgrowth,
        "macroporeflow": _make_macroporeflow,
        "salinitystress": _make_salinitystress,
        "surfacewater": _make_surfacewater,
    }

    return cases[case]()
