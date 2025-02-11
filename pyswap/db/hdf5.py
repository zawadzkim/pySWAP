"""Interacting with HDF5 files.

HDF5 database is meant to store pySWAP models and results in a structured way.
The class allows users to save and load multiple models and results to a single
.h5 file.

Classes:
    HDF5: Class for interacting with HDF5 files.
"""

import logging
import pickle
from typing import Literal

import h5py
import numpy as np
from pydantic import BaseModel, Field, computed_field

from pyswap.model.model import Model
from pyswap.model.result import Result

logger = logging.getLogger(__name__)


class HDF5(BaseModel):
    """Class for interacting with HDF5 files.

    The pySWAP models and results are stored in the HDF5 file as pickled
    objects. These are complete representations of the models and results
    that can be loaded back into memory. They also have some metadata attached
    to them which are stored as atrributes in the HDF5 file. Users can view the
    models in an HDF5 file viewer.

    Attributes:
        filename (str): Path to the HDF5 file.
        models (dict): Dictionary containing the loaded models.
    """

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

        Parameters:
            model (Model): The model to be saved.
            result (Result): The result to be saved.
            overwrite_datasets (bool): If True, overwrite the datasets if they already exist.
            overwrite_project (bool): If True, overwrite the project if it already exists.
            mode (str): The mode in which to save the data. Options are 'python', 'json', and 'yaml'.
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
                logger.info(f"Saved {name} to {group.name}")
            except ValueError:
                logger.warning(
                    f"Cannot create dataset {name} in {group.name}. It may already exist. Skipping creation."
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
    ) -> dict[str, tuple[Model, Result | None]]:
        """Load a single model or all models within a specific project.

        Parameters:
            project (str): The project name.
            model (str): The model name.
            load_results (bool): If True, load the results as well.
            mode (str): The mode in which to load the data. Options are 'python', 'json', and 'yaml'.
        """

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

    def delete(self, project: str, model: str | None = None):
        """Delete a single model or all models within a specific project.

        !!! warning

            Use this method only for small deletions, as for now it does not
            perform repacking of the HDF5 file (the objects are deleted but the
            disk space is not freed). For large deletions, consider creating a
            new HDF5 file and saving only the models you want to keep.

        Parameters:
            project (str): The project name.
            model (str): The model name.
        """
        with h5py.File(self.filename, "a") as f:
            if model is None:
                try:
                    del f[project]
                except KeyError:
                    logger.warning(f"Project {project} does not exist.")
            else:
                try:
                    del f[project][model]
                except KeyError:
                    logger.warning(f"Model {model} does not exist in project {project}.")