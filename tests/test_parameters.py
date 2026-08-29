"""Tests for the declarative parameter addressing core."""

import numpy as np
import pandas as pd
import pytest

import pyswap as psp
from pyswap.parameters import Observation, Observations, Param, ParameterSet


@pytest.fixture
def model():
    ml = psp.Model()
    ml.evaporation = psp.components.soilwater.Evaporation(
        cfevappond=1.25, swcfbs=0, rsoil=30.0, swredu=1, cofredbl=0.35, rsigni=0.5
    )
    soilhydrfunc = psp.components.soilwater.SOILHYDRFUNC.create({
        "ORES": [0.01, 0.02],
        "OSAT": [0.42, 0.38],
        "ALFA": [0.0276, 0.0213],
        "NPAR": [1.491, 1.951],
        "KSATFIT": [12.52, 12.68],
        "LEXP": [-1.060, 0.168],
        "H_ENPR": [0.0, 0.0],
        "KSATEXM": [12.52, 12.68],
        "BDENS": [1315.0, 1315.0],
    })
    soilprofile_table = psp.components.soilwater.SOILPROFILE.create({
        "ISUBLAY": [1, 2],
        "ISOILLAY": [1, 2],
        "HSUBLAY": [10.0, 190.0],
        "HCOMP": [1.0, 5.0],
        "NCOMP": [10, 38],
    })
    ml.soilprofile = psp.components.soilwater.SoilProfile(
        swsophy=0, soilprofile=soilprofile_table, swhyst=0, tau=0.2,
        soilhydrfunc=soilhydrfunc, swmacro=0,
    )
    return ml


def test_apply_scalar_attribute(model):
    ps = ParameterSet([Param("rsoil", "evaporation.rsoil", bounds=(10, 300))])
    new = ps.apply(model, [150.0])

    assert float(new.evaporation.rsoil) == 150.0
    assert float(model.evaporation.rsoil) == 30.0  # original untouched


def test_apply_table_cell(model):
    ps = ParameterSet([
        Param("k_bottom", "soilprofile.soilhydrfunc.KSATFIT[1]", bounds=(0.5, 50))
    ])
    new = ps.apply(model, [4.5])

    table = pd.DataFrame(new.soilprofile.soilhydrfunc)
    assert table.loc[1, "KSATFIT"] == 4.5
    assert table.loc[0, "KSATFIT"] == 12.52
    old = pd.DataFrame(model.soilprofile.soilhydrfunc)
    assert old.loc[1, "KSATFIT"] == 12.68  # original untouched


def test_apply_dict_values(model):
    ps = ParameterSet([
        Param("rsoil", "evaporation.rsoil", bounds=(10, 300)),
        Param("k_top", "soilprofile.soilhydrfunc.KSATFIT[0]", bounds=(0.5, 50)),
    ])
    new = ps.apply(model, {"k_top": 2.0, "rsoil": 60.0})

    assert float(new.evaporation.rsoil) == 60.0
    assert pd.DataFrame(new.soilprofile.soilhydrfunc).loc[0, "KSATFIT"] == 2.0


def test_transform_and_bounds():
    par = Param("k", "evaporation.rsoil", bounds=(0.1, 100.0), transform="log10")

    assert par.to_sample_space(100.0) == pytest.approx(2.0)
    assert par.to_physical(-1.0) == pytest.approx(0.1)
    assert par.sample_bounds == (pytest.approx(-1.0), pytest.approx(2.0))


def test_bad_paths_raise(model):
    with pytest.raises(AttributeError):
        ParameterSet([Param("x", "evaporation.nonsense", bounds=(0, 1))]).apply(
            model, [0.5]
        )
    with pytest.raises(KeyError):
        ParameterSet([
            Param("x", "soilprofile.soilhydrfunc.NOPE[0]", bounds=(0, 1))
        ]).apply(model, [0.5])
    with pytest.raises(ValueError):
        ParameterSet([Param("x", "evaporation.rsoil", bounds=(0, 1))]).apply(
            model, [1.0, 2.0]
        )


def test_observation_residuals():
    idx = pd.date_range("2022-01-01", periods=4)
    observed = pd.Series([1.0, 2.0, 3.0, 4.0], index=idx)
    simulated = pd.Series([1.5, 2.0, 2.0], index=idx[:3])

    obs = Observation("h", observed, simulated=lambda result: simulated, weight=2.0)
    res = obs.residuals(result=None)

    assert list(res) == [1.0, 0.0, -2.0]  # weighted, aligned on common index

    coll = Observations([obs])
    vec = coll.residual_vector(None)
    assert vec.shape == (3,)
    assert coll.rmse(None)["h"] == pytest.approx(np.sqrt((0.5**2 + 0 + 1.0**2) / 3))
