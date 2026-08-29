"""Tests for the estimation layer.

The SWAP executable is not involved: a fake runner returns the applied model
itself as the "result", and observation extractors read the parameter values
back from it — an analytically known inverse problem with a synthetic truth.
"""

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("scipy")

import pyswap as psp
from pyswap.estimation import fit
from pyswap.parameters import Observation, Observations, Param, ParameterSet

TRUTH = {"rsoil": 120.0, "cofredbl": 0.6}


@pytest.fixture
def model():
    ml = psp.Model()
    ml.evaporation = psp.components.soilwater.Evaporation(
        cfevappond=1.25, swcfbs=0, rsoil=30.0, swredu=1, cofredbl=0.35, rsigni=0.5
    )
    return ml


@pytest.fixture
def parameters():
    return ParameterSet([
        Param("rsoil", "evaporation.rsoil", bounds=(10.0, 300.0), transform="log10"),
        Param("cofredbl", "evaporation.cofredbl", bounds=(0.1, 1.0)),
    ])


def fake_runner(applied_model):
    """The 'simulation' is the applied model itself."""
    return applied_model


def synthetic_observations() -> Observations:
    """Observed series generated from the known truth (no noise)."""
    idx = pd.date_range("2022-01-01", periods=10)
    t = np.arange(10, dtype=float)

    def series_from(result):
        a = float(result.evaporation.rsoil)
        b = float(result.evaporation.cofredbl)
        return pd.Series(a * 0.01 * t + b * 5.0, index=idx)

    class _Truth:
        class evaporation:
            rsoil = TRUTH["rsoil"]
            cofredbl = TRUTH["cofredbl"]

    observed = series_from(_Truth)
    return Observations([Observation("y", observed, simulated=series_from)])


def test_least_squares_recovers_truth(model, parameters):
    fr = fit(
        model, parameters, synthetic_observations(),
        method="least_squares", _runner=fake_runner,
    )

    assert fr.success
    assert fr.values[0] == pytest.approx(TRUTH["rsoil"], rel=1e-3)
    assert fr.values[1] == pytest.approx(TRUTH["cofredbl"], rel=1e-3)
    assert fr.rmse["y"] == pytest.approx(0.0, abs=1e-6)
    assert float(fr.model.evaporation.rsoil) == pytest.approx(TRUTH["rsoil"], rel=1e-3)
    assert fr.se is not None
    assert list(fr.correlation.columns) == ["rsoil", "cofredbl"]
    assert set(fr.summary().columns) == {"name", "value", "se_sample_space"}


def test_differential_evolution_recovers_truth(model, parameters):
    fr = fit(
        model, parameters, synthetic_observations(),
        method="differential_evolution", _runner=fake_runner,
        seed=1, maxiter=60, tol=1e-8,
    )

    assert fr.values[0] == pytest.approx(TRUTH["rsoil"], rel=1e-2)
    assert fr.values[1] == pytest.approx(TRUTH["cofredbl"], rel=1e-2)
    assert fr.se is None


def test_failed_run_raises(model, parameters):
    def failing_runner(applied_model):
        return None

    with pytest.raises(RuntimeError, match="run failed"):
        fit(model, parameters, synthetic_observations(),
            method="least_squares", _runner=failing_runner)


def test_unknown_method_raises(model, parameters):
    with pytest.raises(ValueError, match="unknown method"):
        fit(model, parameters, synthetic_observations(),
            method="nonsense", _runner=fake_runner)
