"""Parameter estimation on top of the parameter core.

`fit` minimizes the weighted residuals of a set of observations by adjusting
a `ParameterSet`, working in the parameters' sampling space (transforms
respected) and applying values to the model through the parameter core.

The first backends are scipy's trust-region least squares (local, with a
linearized covariance from the Jacobian) and differential evolution (global,
covariance-free); further backends (spotpy samplers, PEST++ export) are
planned to slot into the same signature.

Practical notes for SWAP models: the numerical Jacobian is built from finite
differences, and the model's iterative solver introduces noise at small
steps — keep `diff_step` coarse (the default is 1e-2 relative) rather than
letting scipy shrink it. Standard errors come from the linearized covariance
at the optimum and inherit its assumptions (local quadratic cost, independent
residuals); autocorrelated daily residuals make them optimistic.

Requires the `pe` extra: ``pip install pyswap[pe]``.

Classes:
    FitResult: Container for the estimate and its diagnostics.

Functions:
    fit: Estimate parameters against observations.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

from pyswap.parameters import Observations, ParameterSet

if TYPE_CHECKING:
    from pyswap.model.model import Model
    from pyswap.model.result import Result

__all__ = ["FitResult", "fit"]


def _require_scipy():
    try:
        import scipy  # noqa: F401
    except ImportError as err:
        msg = (
            "parameter estimation requires scipy; "
            "install it with `pip install pyswap[pe]`"
        )
        raise ImportError(msg) from err


@dataclass
class FitResult:
    """The estimate and its diagnostics.

    Attributes:
        names: Parameter names, ordering all arrays below.
        values: Estimated values in physical units.
        se: Linearized standard errors in sampling space (None for
            covariance-free backends); for log10-transformed parameters this
            is the standard error of the decadic logarithm.
        correlation: Parameter correlation matrix (None when unavailable).
        rmse: Unweighted RMSE per observation at the optimum.
        model: The model with the estimated values applied.
        result: The simulation result at the optimum.
        nfev: Number of model evaluations spent.
        success: Whether the optimizer reported convergence.
        message: The optimizer's status message.
        raw: The underlying scipy result object.
    """

    names: list[str]
    values: list[float]
    se: list[float] | None
    correlation: pd.DataFrame | None
    rmse: dict[str, float]
    model: Model
    result: Result
    nfev: int
    success: bool
    message: str
    raw: object

    def summary(self) -> pd.DataFrame:
        """One row per parameter: value and (sampling-space) standard error."""
        return pd.DataFrame({
            "name": self.names,
            "value": self.values,
            "se_sample_space": self.se if self.se is not None else np.nan,
        })


def _default_runner(model: Model) -> Result:
    return model.run(silence_warnings=True)


def fit(
    model: Model,
    parameters: ParameterSet,
    observations: Observations,
    method: Literal["least_squares", "differential_evolution"] = "least_squares",
    x0: list[float] | None = None,
    diff_step: float = 1e-2,
    _runner: Callable[[Model], Result] | None = None,
    **kwargs,
) -> FitResult:
    """Estimate parameters against observations.

    Parameters:
        model: The base model the estimate derives from.
        parameters: The parameters to estimate (bounds and transforms apply).
        observations: The observations whose weighted residuals are minimized.
        method: ``"least_squares"`` (local, with covariance) or
            ``"differential_evolution"`` (global, covariance-free).
        x0: Starting values in physical units (least squares only; default is
            the midpoint of the sampling-space bounds).
        diff_step: Relative finite-difference step for the Jacobian; keep it
            coarse for models with iterative-solver noise.
        kwargs: Passed through to the scipy optimizer.

    Returns:
        A `FitResult`.
    """
    _require_scipy()
    from scipy import optimize

    runner = _runner if _runner is not None else _default_runner
    lo = np.array([p.sample_bounds[0] for p in parameters.params])
    hi = np.array([p.sample_bounds[1] for p in parameters.params])

    def to_physical(x: np.ndarray) -> list[float]:
        return [
            p.to_physical(float(v))
            for p, v in zip(parameters.params, x, strict=True)
        ]

    def run_at(x: np.ndarray) -> Result:
        applied = parameters.apply(model, to_physical(x))
        result = runner(applied)
        if result is None:
            msg = f"model run failed at {dict(zip(parameters.names, to_physical(x), strict=True))}"
            raise RuntimeError(msg)
        return result

    if method == "least_squares":

        def residuals(x: np.ndarray) -> np.ndarray:
            return observations.residual_vector(run_at(x))

        if x0 is None:
            start = (lo + hi) / 2.0
        else:
            start = np.array([
                p.to_sample_space(v)
                for p, v in zip(parameters.params, x0, strict=True)
            ])
        raw = optimize.least_squares(
            residuals, start, bounds=(lo, hi), diff_step=diff_step, **kwargs
        )
        x_opt, nfev = raw.x, raw.nfev
        se, correlation = _linearized_uncertainty(raw, parameters.names)

    elif method == "differential_evolution":

        def cost(x: np.ndarray) -> float:
            try:
                r = observations.residual_vector(run_at(x))
            except RuntimeError:
                return np.inf
            return float(0.5 * (r**2).sum())

        raw = optimize.differential_evolution(
            cost, bounds=list(zip(lo, hi, strict=True)), **kwargs
        )
        x_opt, nfev = raw.x, raw.nfev
        se, correlation = None, None

    else:
        msg = f"unknown method '{method}'"
        raise ValueError(msg)

    best_values = to_physical(x_opt)
    best_model = parameters.apply(model, best_values)
    best_result = runner(best_model)

    return FitResult(
        names=parameters.names,
        values=best_values,
        se=se,
        correlation=correlation,
        rmse=observations.rmse(best_result),
        model=best_model,
        result=best_result,
        nfev=int(nfev),
        success=bool(raw.success),
        message=str(raw.message),
        raw=raw,
    )


def _linearized_uncertainty(raw, names: list[str]):
    """Standard errors and correlation from the least-squares Jacobian."""
    jac = raw.jac
    m, n = jac.shape
    dof = max(m - n, 1)
    s2 = 2.0 * raw.cost / dof
    try:
        cov = np.linalg.inv(jac.T @ jac) * s2
    except np.linalg.LinAlgError:
        return None, None
    se = np.sqrt(np.clip(np.diag(cov), 0.0, None))
    denom = np.outer(se, se)
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = np.where(denom > 0, cov / denom, np.nan)
    return (
        [float(v) for v in se],
        pd.DataFrame(corr, index=names, columns=names),
    )
