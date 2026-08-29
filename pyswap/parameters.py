"""Declarative parameter addressing for sensitivity analysis and estimation.

This module is the shared core of the model-analysis tooling: it defines how a
named parameter maps onto a location inside a `Model`, how a set of parameter
values is applied to produce a new model, and how observed series are compared
against simulation results.

The sensitivity (`pyswap.sensitivity`) and estimation (`pyswap.estimation`)
layers consume these objects; they contain no addressing logic of their own.

Paths address two kinds of locations:

- component attributes, dotted from the model root, e.g.
  ``"evaporation.rsoil"`` or ``"lateraldrainage.drafile.fluxes.drares1"``;
- table cells, with the column name and integer row index as the final
  segment, e.g. ``"soilprofile.soilhydrfunc.KSATFIT[2]"``.

Compound parameters (one value driving several locations) are not expressible
as a single path; list one parameter per location instead.

Classes:
    Param: One named, bounded parameter addressing a location in the model.
    ParameterSet: An ordered collection of parameters.
    Observation: An observed series paired with an extractor of its simulated
        counterpart.
    Observations: A collection of observations producing residual vectors.

Functions:
    evaluate: Run the model for a batch of parameter samples.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from pyswap.model.model import Model
    from pyswap.model.result import Result

__all__ = ["Observation", "Observations", "Param", "ParameterSet", "evaluate"]

_CELL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\[(\d+)\]$")


@dataclass(frozen=True)
class Param:
    """One named, bounded parameter addressing a location in the model.

    Attributes:
        name: Identifier used in samples, results and reports.
        path: Dotted path from the model root (see module docstring).
        bounds: Lower and upper bound in physical (untransformed) units.
        transform: Optional sampling-space transform; samplers and optimizers
            work in transformed space, `ParameterSet.apply` always takes
            physical values.
    """

    name: str
    path: str
    bounds: tuple[float, float]
    transform: Literal["log10"] | None = None

    def to_sample_space(self, value: float) -> float:
        """Physical value -> sampling/optimization space."""
        if self.transform == "log10":
            return math.log10(value)
        return value

    def to_physical(self, value: float) -> float:
        """Sampling/optimization space -> physical value."""
        if self.transform == "log10":
            return 10.0**value
        return value

    @property
    def sample_bounds(self) -> tuple[float, float]:
        """The bounds expressed in sampling space."""
        lo, hi = self.bounds
        return (self.to_sample_space(lo), self.to_sample_space(hi))


def _set_by_path(obj, segments: list[str], value: float):
    """Return a copy of a pyswap object with the addressed location replaced.

    Works recursively: each level is rebuilt through the object's `update`
    method so that pydantic validation stays in force.
    """
    head, rest = segments[0], segments[1:]

    cell = _CELL_RE.match(head)
    if cell:
        if rest:
            msg = f"table cell must be the final path segment, got {segments}"
            raise ValueError(msg)
        column, row = cell.group(1), int(cell.group(2))
        if not isinstance(obj, pd.DataFrame):
            msg = f"cell addressing '{head}' requires a table, got {type(obj)}"
            raise TypeError(msg)
        if column not in obj.columns:
            msg = f"column '{column}' not found in table {list(obj.columns)}"
            raise KeyError(msg)
        table = obj.copy()
        table.iloc[row, table.columns.get_loc(column)] = value
        return table

    if not hasattr(obj, head):
        msg = f"'{type(obj).__name__}' has no attribute '{head}'"
        raise AttributeError(msg)

    if not rest:
        return obj.update({head: value})

    child = getattr(obj, head)
    if child is None:
        msg = f"attribute '{head}' is not set on '{type(obj).__name__}'"
        raise AttributeError(msg)
    return obj.update({head: _set_by_path(child, rest, value)})


@dataclass
class ParameterSet:
    """An ordered collection of parameters applied to a model together."""

    params: list[Param]

    @property
    def names(self) -> list[str]:
        return [p.name for p in self.params]

    @property
    def bounds(self) -> list[tuple[float, float]]:
        return [p.bounds for p in self.params]

    def __len__(self) -> int:
        return len(self.params)

    def apply(self, model: Model, values) -> Model:
        """Return a new model with the parameter values (physical units) set.

        Parameters:
            model: The model to derive from; it is not modified.
            values: A sequence ordered like `params`, or a name-to-value dict.
        """
        if isinstance(values, dict):
            missing = set(self.names) - set(values)
            if missing:
                msg = f"missing values for parameters: {sorted(missing)}"
                raise ValueError(msg)
            values = [values[n] for n in self.names]
        if len(values) != len(self.params):
            msg = f"expected {len(self.params)} values, got {len(values)}"
            raise ValueError(msg)

        for par, val in zip(self.params, values):
            segments = par.path.split(".")
            model = model.update({
                segments[0]: _set_by_path(
                    getattr(model, segments[0]), segments[1:], float(val)
                )
            })
        return model


@dataclass
class Observation:
    """An observed series paired with an extractor of its simulated twin.

    Attributes:
        name: Identifier used in reports.
        observed: The observed series (datetime-indexed).
        simulated: Callable mapping a `Result` to the comparable series.
        weight: Multiplier applied to the residuals of this observation.
    """

    name: str
    observed: pd.Series
    simulated: Callable[[Result], pd.Series]
    weight: float = 1.0

    def residuals(self, result: Result) -> pd.Series:
        """Weighted residuals (simulated - observed) on the common index."""
        sim = self.simulated(result)
        both = pd.concat(
            [sim.rename("sim"), self.observed.rename("obs")], axis=1
        ).dropna()
        return (both["sim"] - both["obs"]) * self.weight


@dataclass
class Observations:
    """A collection of observations producing one residual vector."""

    observations: list[Observation] = field(default_factory=list)

    def residual_vector(self, result: Result) -> np.ndarray:
        """All weighted residuals concatenated into one array."""
        parts = [o.residuals(result).to_numpy() for o in self.observations]
        return np.concatenate(parts) if parts else np.array([])

    def rmse(self, result: Result) -> dict[str, float]:
        """Unweighted RMSE per observation."""
        out = {}
        for o in self.observations:
            r = o.residuals(result) / (o.weight if o.weight else 1.0)
            out[o.name] = float(np.sqrt((r**2).mean()))
        return out


def evaluate(
    model: Model,
    parameters: ParameterSet,
    samples,
    silence_warnings: bool = True,
    **kwargs,
) -> list[Result]:
    """Run the model for a batch of parameter samples (physical units).

    Parameters:
        model: The base model every sample derives from.
        parameters: The parameter set the sample columns map onto.
        samples: 2D array-like, one row per sample.
        silence_warnings: Passed through to the runner.
        kwargs: Passed through to `run_parallel`.

    Returns:
        One `Result` per row, in order (None where a run failed).
    """
    from pyswap.model.model import run_parallel

    models = [parameters.apply(model, row) for row in np.atleast_2d(samples)]
    return run_parallel(models, silence_warnings=silence_warnings, **kwargs)
