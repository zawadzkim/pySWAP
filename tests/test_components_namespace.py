import importlib

import pyswap as ps
from pyswap import components

SUBMODULES = [
    "boundary",
    "crop",
    "drainage",
    "irrigation",
    "meteorology",
    "simsettings",
    "soilwater",
    "transport",
]


def test_component_classes_are_reexported():
    assert ps.components.Meteorology is ps.components.meteorology.Meteorology
    assert ps.components.MetFile is ps.components.meteorology.MetFile
    assert ps.components.metfile_from_csv is ps.components.meteorology.metfile_from_csv
    assert ps.components.SoilProfile is ps.components.soilwater.SoilProfile


def test_every_public_class_of_the_submodules_is_reexported():
    for name in SUBMODULES:
        module = importlib.import_module(f"pyswap.components.{name}")
        for obj_name in module.__all__:
            obj = getattr(module, obj_name)
            if obj_name.isupper() or obj_name.startswith("_"):
                continue  # tables stay in their submodule; private bases too
            if not isinstance(obj, type):
                continue
            assert getattr(components, obj_name) is obj, f"{name}.{obj_name}"
            assert obj_name in components.__all__


def test_top_level_namespace_is_not_flattened():
    assert not hasattr(ps, "Meteorology")
