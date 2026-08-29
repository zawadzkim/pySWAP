"""Tests for the one-call sensitivity workflows.

The SWAP executable is not involved: a fake evaluator hands the applied
physical parameter values back as the "results", and analytical responses
with known sensitivity structure verify the plumbing (sampling, transforms,
multi-output handling, tidy output shape).
"""

import numpy as np
import pytest

pytest.importorskip("SALib")

from pyswap.parameters import Param, ParameterSet
from pyswap.sensitivity import run_morris, run_sobol


@pytest.fixture
def parameters():
    return ParameterSet([
        Param("weak", "evaporation.rsoil", bounds=(0.0, 1.0)),
        Param("strong", "evaporation.rsigni", bounds=(0.0, 1.0)),
    ])


def fake_evaluator(model, parameters, samples, silence_warnings=True, **kwargs):
    """Return the physical parameter vectors themselves as 'results'."""
    return [np.asarray(row) for row in np.atleast_2d(samples)]


def linear_response(result):
    """Strongly dominated by the second parameter."""
    return float(result[0] + 10.0 * result[1])


def test_morris_ranks_parameters(parameters):
    df = run_morris(
        None, parameters, linear_response,
        trajectories=8, seed=1, _evaluator=fake_evaluator,
    )

    assert set(df.columns) == {"output", "name", "mu_star", "mu_star_conf", "mu", "sigma"}
    assert list(df["name"]) == ["weak", "strong"]
    mu = df.set_index("name")["mu_star"]
    assert mu["strong"] > 5 * mu["weak"]


def test_sobol_ranks_parameters(parameters):
    df = run_sobol(
        None, parameters, linear_response, n=64, seed=1, _evaluator=fake_evaluator
    )

    st = df.set_index("name")["ST"]
    assert st["strong"] > 0.9
    assert st["weak"] < 0.1


def test_multi_output_is_tidy(parameters):
    def response(result):
        return {"a": float(result[0]), "b": float(result[1])}

    df = run_morris(
        None, parameters, response, trajectories=4, seed=1, _evaluator=fake_evaluator
    )

    assert sorted(df["output"].unique()) == ["a", "b"]
    assert len(df) == 4  # 2 outputs x 2 parameters
    # each output is dominated by its own parameter
    a = df[df.output == "a"].set_index("name")["mu_star"]
    assert a["weak"] > a["strong"]


def test_transforms_are_respected():
    ps = ParameterSet([
        Param("k", "evaporation.rsoil", bounds=(0.01, 100.0), transform="log10"),
    ])
    seen = []

    def spy_evaluator(model, parameters, samples, **kwargs):
        seen.extend(np.atleast_2d(samples)[:, 0].tolist())
        return list(np.atleast_2d(samples))

    run_morris(None, ps, lambda r: float(r[0]), trajectories=4, seed=1,
               _evaluator=spy_evaluator)

    assert min(seen) >= 0.01 and max(seen) <= 100.0  # physical units reach the model
    assert min(seen) < 0.5  # log sampling actually visits the low decades


def test_failed_runs_raise(parameters):
    def failing_evaluator(model, parameters, samples, **kwargs):
        results = [np.asarray(r) for r in np.atleast_2d(samples)]
        results[1] = None
        return results

    with pytest.raises(RuntimeError, match="runs failed"):
        run_morris(None, parameters, linear_response, trajectories=4, seed=1,
                   _evaluator=failing_evaluator)
