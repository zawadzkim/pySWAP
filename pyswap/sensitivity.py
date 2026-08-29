"""One-call sensitivity analysis on top of the parameter core.

Both entry points sample in the parameters' sampling space (transforms
respected), run the model batch through `pyswap.parameters.evaluate`, reduce
every result to one or more named responses, and hand the matrices to SALib.
They return tidy DataFrames — one row per (output, parameter) — and produce
no plots; plotting belongs to the analysis notebooks.

Recommended workflow: screen with `run_morris` first to find the parameters
the responses can actually see, then spend the Sobol budget on that subset.

Requires the `sa` extra: ``pip install pyswap[sa]``.

Functions:
    run_morris: Morris elementary-effects screening.
    run_sobol: Sobol variance decomposition (Saltelli sampling).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from pyswap.parameters import ParameterSet, evaluate

if TYPE_CHECKING:
    from pyswap.model.model import Model
    from pyswap.model.result import Result

__all__ = ["run_morris", "run_sobol"]


def _require_salib():
    try:
        import SALib  # noqa: F401
    except ImportError as err:
        msg = (
            "sensitivity analysis requires SALib; "
            "install it with `pip install pyswap[sa]`"
        )
        raise ImportError(msg) from err


def _problem(parameters: ParameterSet) -> dict:
    """The SALib problem dict, with bounds in sampling space."""
    return {
        "num_vars": len(parameters),
        "names": parameters.names,
        "bounds": [list(p.sample_bounds) for p in parameters.params],
    }


def _responses(
    model: Model,
    parameters: ParameterSet,
    sample: np.ndarray,
    response: Callable[[Result], float | dict[str, float]],
    silence_warnings: bool,
    _evaluator: Callable | None,
) -> dict[str, np.ndarray]:
    """Physical-space evaluation of a sampling-space matrix -> named Y arrays."""
    physical = np.column_stack([
        [p.to_physical(v) for v in sample[:, j]]
        for j, p in enumerate(parameters.params)
    ])
    evaluator = _evaluator if _evaluator is not None else evaluate
    results = evaluator(model, parameters, physical, silence_warnings=silence_warnings)

    failed = [i for i, r in enumerate(results) if r is None]
    if failed:
        msg = (
            f"{len(failed)} of {len(results)} runs failed (sample rows "
            f"{failed[:10]}{'...' if len(failed) > 10 else ''}); sensitivity "
            "matrices must be complete."
        )
        raise RuntimeError(msg)

    rows = []
    for r in results:
        value = response(r)
        rows.append(value if isinstance(value, dict) else {"response": value})

    outputs = list(rows[0])
    return {out: np.array([row[out] for row in rows], dtype=float) for out in outputs}


def run_morris(
    model: Model,
    parameters: ParameterSet,
    response: Callable[[Result], float | dict[str, float]],
    trajectories: int = 20,
    levels: int = 4,
    seed: int | None = None,
    silence_warnings: bool = True,
    _evaluator: Callable | None = None,
) -> pd.DataFrame:
    """Morris elementary-effects screening.

    Cost: ``trajectories * (len(parameters) + 1)`` model runs.

    Parameters:
        model: The base model every sample derives from.
        parameters: The parameters to screen.
        response: Callable reducing a `Result` to a float or a dict of named
            floats (one screening per name).
        trajectories: Number of Morris trajectories.
        levels: Number of grid levels.
        seed: Random seed for the sampler.
        silence_warnings: Passed through to the runner.

    Returns:
        Tidy DataFrame with columns ``output, name, mu_star, mu_star_conf,
        mu, sigma``, one row per (output, parameter).
    """
    _require_salib()
    from SALib.analyze import morris as morris_analyze
    from SALib.sample import morris as morris_sample

    problem = _problem(parameters)
    sample = morris_sample.sample(
        problem, N=trajectories, num_levels=levels, seed=seed
    )
    ys = _responses(model, parameters, sample, response, silence_warnings, _evaluator)

    frames = []
    for output, y in ys.items():
        si = morris_analyze.analyze(problem, sample, y, num_levels=levels, seed=seed)
        frames.append(
            pd.DataFrame({
                "output": output,
                "name": problem["names"],
                "mu_star": si["mu_star"],
                "mu_star_conf": si["mu_star_conf"],
                "mu": si["mu"],
                "sigma": si["sigma"],
            })
        )
    return pd.concat(frames, ignore_index=True)


def run_sobol(
    model: Model,
    parameters: ParameterSet,
    response: Callable[[Result], float | dict[str, float]],
    n: int = 256,
    seed: int | None = None,
    silence_warnings: bool = True,
    _evaluator: Callable | None = None,
) -> pd.DataFrame:
    """Sobol variance decomposition with Saltelli sampling.

    Cost: ``n * (len(parameters) + 2)`` model runs; ``n`` must be a power
    of two.

    Parameters:
        model: The base model every sample derives from.
        parameters: The parameters to decompose over.
        response: Callable reducing a `Result` to a float or a dict of named
            floats (one decomposition per name).
        n: Saltelli base sample size (power of two).
        seed: Random seed for the sampler.
        silence_warnings: Passed through to the runner.

    Returns:
        Tidy DataFrame with columns ``output, name, S1, S1_conf, ST,
        ST_conf``, one row per (output, parameter).
    """
    _require_salib()
    from SALib.analyze import sobol as sobol_analyze
    from SALib.sample import sobol as sobol_sample

    problem = _problem(parameters)
    sample = sobol_sample.sample(problem, N=n, calc_second_order=False, seed=seed)
    ys = _responses(model, parameters, sample, response, silence_warnings, _evaluator)

    frames = []
    for output, y in ys.items():
        si = sobol_analyze.analyze(problem, y, calc_second_order=False, seed=seed)
        frames.append(
            pd.DataFrame({
                "output": output,
                "name": problem["names"],
                "S1": si["S1"],
                "S1_conf": si["S1_conf"],
                "ST": si["ST"],
                "ST_conf": si["ST_conf"],
            })
        )
    return pd.concat(frames, ignore_index=True)
