# ruff: noqa: S301, TRY300
# mypy: disable-error-code="operator, index"
# operator and index errors were showing up in the _load_pickled method. This
# should be observed and fixed in the future if needed.

# Perhaps in the next versions, we can implement methods to handle pickes more
# safely. For now, it's not a high priority.
# Error TRY300 also seemed a bit too strict for this case.
"""Interacting with HDF5 files.

HDF5 database is meant to store pySWAP models and results in a structured way.
The class allows users to save and load multiple models and results to a single
.h5 file.

Classes:
    HDF5: Class for interacting with HDF5 files.
"""

import logging
import pickle
from typing import TYPE_CHECKING, Literal, Union

import h5py
import numpy as np
from pydantic import BaseModel, Field, computed_field

if TYPE_CHECKING:
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
            models = {project: list(f[project].keys()) for project in f}
        return models

    @staticmethod
    def _get_or_create_group(f, group_name):
        """Get a group from an HDF5 file or create it if it does not exist."""
        return f.require_group(group_name)

    def save_model(
        self,
        model: "Model",
        result: Union["Result", None] = None,
        overwrite_datasets: bool = False,
        overwrite_project: bool = False,
        mode: Literal["python", "json", "yaml", "plain"] = "python",
    ):
        """
        Save a model and its results to an HDF5 file.

        Parameters:
            model (Model): The model to be saved.
            result (Result, optional): The result to be saved.
            overwrite_datasets (bool): If True, overwrite datasets if they exist.
            overwrite_project (bool): If True, overwrite the project if it exists.
            mode (Literal["python", "json", "yaml"]): The format in which to save the data.
                Only 'python' is currently supported.

        Raises:
            NotImplementedError: If 'json' or 'yaml' modes are selected.
        """
        with h5py.File(self.filename, "a") as f:
            # Handle project overwriting
            if overwrite_project:
                self._overwrite_project(f, model.metadata.project)

            # Create or retrieve project group
            project_group = self._get_or_create_group(f, model.metadata.project)
            self._update_attributes(project_group, model.metadata.__dict__)

            # Create or retrieve model group
            model_group = self._get_or_create_group(project_group, model.version)

            # Handle dataset overwriting
            if overwrite_datasets:
                self._overwrite_datasets(model_group)

            # Save data based on the mode
            if mode == "python":
                self._save_pickled(model_group, "input", model)
                if result:
                    self._save_pickled(model_group, "output", result)
            else:
                raise NotImplementedError(f"Mode '{mode}' is not yet implemented.")

    def load(
        self,
        project: str,
        model: str | None = None,
        load_results: bool = False,
        mode: Literal["python", "json", "yaml"] = "python",
    ) -> dict[str, tuple["Model", Union["Result", None]]]:
        """
        Load a single model or all models within a specific project.

        Parameters:
            project (str): The project name.
            model (str, optional): The model name. If None, loads all models in the project.
            load_results (bool): Whether to load results along with the model.
            mode (Literal["python", "json", "yaml"]): The format in which to load the data.
                Only 'python' is currently supported.

        Returns:
            dict[str, tuple[Model, Union[Result, None]]]: A dictionary of loaded models and their results.

        Raises:
            NotImplementedError: If 'json' or 'yaml' modes are selected.
        """
        loaded_models = {}

        with h5py.File(self.filename, "r") as f:
            # Validate that the project exists
            if project not in f:
                msg = f"Project '{project}' does not exist in the HDF5 file."
                raise KeyError(msg)

            # Get all models in the project
            all_models = self.list_models[project]

            if mode == "python":
                # Load all models if no specific model is provided
                if model is None:
                    for item in all_models:
                        loaded_models[item] = self._load_pickled(
                            group=f[project], name=item, load_results=load_results
                        )
                else:
                    # Validate that the specific model exists
                    if model not in all_models:
                        msg = f"Model '{model}' does not exist in project '{project}'."
                        raise KeyError(msg)
                    loaded_models[model] = self._load_pickled(
                        group=f[project], name=model, load_results=load_results
                    )
            else:
                msg = f"Mode '{mode}' is not yet implemented."
                raise NotImplementedError(msg)

        # Update internal models dictionary and return loaded models
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
                    logger.warning(
                        f"Model {model} does not exist in project {project}."
                    )

    def _overwrite_datasets(self, group):
        """Delete all datasets within a group."""
        for key in list(group.keys()):
            try:
                del group[key]
                logger.info(f"Deleted dataset {key} in group {group.name}")
            except KeyError:
                logger.warning(f"Failed to delete dataset {key} in group {group.name}")

    def _overwrite_project(self, file, project_name):
        """Delete a project group from the HDF5 file."""
        try:
            del file[project_name]
            logger.info(f"Deleted project {project_name}")
        except KeyError:
            logger.warning(f"Project {project_name} does not exist.")

    def _save_plain_string(self, group, name, data):
        """Save data as a plain string dataset."""

    def _save_pickled(self, group, name, data):
        """Save data as a pickled dataset."""
        try:
            pickle_data = pickle.dumps(data)
            group.create_dataset(name, data=np.void(pickle_data))
            logger.info(f"Saved {name} to {group.name}")
        except ValueError as e:
            logger.warning(
                f"Failed to create dataset {name} in {group.name}. Error: {e}"
            )

    def _update_attributes(self, group, attributes):
        """Update attributes of an HDF5 group."""
        sanitized_attrs = {k: v for k, v in attributes.items() if v is not None}
        group.attrs.update(sanitized_attrs)

    def _load_pickled(
        self, group: h5py.Group, name: str, load_results: bool
    ) -> tuple["Model", Union["Result", None]]:
        """
        Load a pickled model and optionally its results from an HDF5 group.

        Parameters:
            group (h5py.Group): The HDF5 group containing the model data.
            name (str): The name of the model to load.
            load_results (bool): Whether to load results along with the model.

        Returns:
            tuple[Model, Union[Result, None]]: The loaded model and its results (if applicable).
        """
        try:
            # Load pickled input data
            pickle_in = group[name]["input"][()].tobytes()
            model: Model = pickle.loads(pickle_in)

            # Optionally load pickled output data
            result: Result = None

            if load_results and "output" in group[name]:
                pickle_out = group[name]["output"][()].tobytes()
                result = pickle.loads(pickle_out)

            logger.info(f"Loaded model '{name}' from group '{group.name}'.")
            return model, result
        except Exception:
            logger.exception(f"Failed to load model '{name}' from group '{group.name}'")
            return None, None
