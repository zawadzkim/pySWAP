"""This file contains classes and functions for handling HDF5 integration."""

import logging
import pickle
from typing import Literal

import h5py
import numpy as np
from pydantic import BaseModel, Field, computed_field

from pyswap.model import Model, Result

logger = logging.getLogger(__name__)


class HDF5(BaseModel):
    filename: str
    models: dict | None = Field(default_factory=dict)

    @computed_field(return_type=dict)
    def list_projects(self):
        """List all the projects in the HDF5 file."""
        with h5py.File(self.filename, "r") as f:
            projects = list(f.keys())
        return projects

    @computed_field(return_type=dict)
    def list_models(self):
        """List all the models in the HDF5 file."""
        with h5py.File(self.filename, "r") as f:
            # Use the visititems method to traverse the file structure
            models = {project: list(f[project].keys()) for project in f.keys()}
        return models

    @staticmethod
    def _get_or_create_group(f, group_name):
        """Get a group from an HDF5 file or create it if it does not exist."""
        if group_name not in f:
            try:
                f.create_group(group_name)
            except ValueError:
                logger.warning(
                    f"Cannot create group {group_name}. It may already exist. Skipping creation."
                )
        return f.require_group(group_name)

    def save_model(
        self,
        model: Model,
        result: Result | None = None,
        overwrite_datasets: bool = False,
        overwrite_project: bool = False,
        mode: Literal["python", "json", "yaml"] = "python",
    ):
        """Sava a model and its results to an HDF5 file.

        Each model in its metadata attribute stores the project name. That is used as the name for the main group. If that name already exists,
        a new group is not created. Then the check is made if the version of the model already exists. If it does, the group is not created.
        """

        def _overwrite_datasets(group):
            for key in list(group.keys()):
                try:
                    del group[key]
                except KeyError:
                    pass

        def _overwrite_project(f, project_name):
            try:
                del f[project_name]
            except KeyError:
                pass

        def _save_pickled(group, name, data):
            try:
                pickle_data = pickle.dumps(data)
                group.create_dataset(name, data=np.void(pickle_data))
            except ValueError:
                logger.warning(
                    f"Cannot create dataset {name}. It may already exist. Skipping creation."
                )

        with h5py.File(self.filename, "a") as f:
            if overwrite_project:
                _overwrite_project(f, model.metadata.project)
            # create a project and add attributes
            project_group = self._get_or_create_group(f, model.metadata.project)
            project_attrs = model.metadata.__dict__
            project_attrs = {k: v for k, v in project_attrs.items() if v is not None}

            project_group.attrs.update(project_attrs)

            # create a model group with input and output datasets
            model_group = self._get_or_create_group(project_group, model.version)

            if overwrite_datasets:
                _overwrite_datasets(model_group)

            if mode == "python":
                # For the python option there is no need for an additional group
                _save_pickled(model_group, "input", model)
                if result:
                    _save_pickled(model_group, "output", result)

            if mode == "json":
                raise NotImplementedError("JSON mode is not yet implemented")

            if mode == "yaml":
                raise NotImplementedError("YAML mode is not yet implemented")

    def load(
        self,
        project: str,
        model: str | None = None,
        load_results: bool = False,
        mode: Literal["python", "json", "yaml"] = "python",
    ) -> dict:
        """Load a single model or all models within a specific project."""

        def _load_pickled(
            group: h5py.Group, name: str, load_results: bool
        ) -> tuple[Model, Result | None]:
            pickle_in = group[name]["input"][()].tobytes()
            pickle_out = (
                group[name]["output"][()].tobytes()
                if load_results and "output" in group[name]
                else None
            )

            model = pickle.loads(pickle_in)
            result = pickle.loads(pickle_out) if pickle_out else None
            return model, result

        loaded_models = {}

        all_models = self.list_models[project]

        with h5py.File(self.filename, "r") as f:
            if mode == "python":
                if model is None:
                    for item in all_models:
                        loaded_models[item] = _load_pickled(
                            group=f[project], name=item, load_results=load_results
                        )
                else:
                    loaded_models[model] = _load_pickled(
                        group=f[project], name=model, load_results=load_results
                    )

            if mode == "json":
                raise NotImplementedError("JSON mode is not yet implemented")

            if mode == "yaml":
                raise NotImplementedError("YAML mode is not yet implemented")

        self.models.update(loaded_models)
        return loaded_models

