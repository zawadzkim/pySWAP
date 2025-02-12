# mypy: disable-error-code="attr-defined"

import pyswap as psp
from pyswap import testcase


def _make_grassgrowth():
    """Loading the grassgrowth model from ascii files."""
    meta = psp.components.Metadata(
        author="John Doe",
        institution="University of Somewhere",
        email="john.doe@somewhere.com",
        project="pySWAP test - hupselbrook",
        swap_ver="4.2",
    )

    ml = psp.load_swp(testcase.get_path("grassgrowth", "swp"), meta)
    ml.bottomboundary = psp.load_bbc(
        testcase.get_path("grassgrowth", "bbc"), ml.bottomboundary
    )

    ml.crop.cropfiles = {
        "grassd": psp.load_crp(
            testcase.get_path("grassgrowth", "grassd"), crptype="grass", name="grassd"
        )
    }

    ml.lateraldrainage.drafile = psp.load_dra(testcase.get_path("grassgrowth", "dra"))

    ml.meteorology.metfile = psp.components.meteorology.metfile_from_csv(
        "260.met", testcase.get_path("grassgrowth", "met")
    )
    return ml
