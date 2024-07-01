"""This file contains classes and functions for handling HDF5 integration."""
import h5py
from typing import Literal, Optional
from pyswap.model import Model, Result
from typing import Tuple
import numpy as np
import pickle
from pydantic import BaseModel, computed_field, Field


class HDF5(BaseModel):

    filename: str
    models: Optional[dict] = Field(default_factory=dict)

    @computed_field(return_type=dict)
    def list_projects(self):
        with h5py.File(self.filename, 'a') as f:
            # Use the visititems method to traverse the file structure
            projects = list(f.keys())
        return projects

    @staticmethod
    def _get_or_create_group(f, group_name):
        if group_name not in f:
            try:
                f.create_group(group_name)
            except ValueError:
                raise ValueError(
                    f'Cannot create group {group_name}. It may already exist. If you want to overwrite it, set overwrite=True.')
        return f[group_name]

    def save_model(self,
                   model: Model,
                   result: Optional[Result] = None,
                   overwrite_datasets: bool = False,
                   overwrite_project: bool = False,
                   mode: Literal['python', 'json', 'yaml'] = 'python'):
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
                raise ValueError(
                    f'Cannot create dataset {name}. It may already exist. If you want to overwrite it, set overwrite=True.')

        with h5py.File(self.filename, 'a') as f:

            if overwrite_project:
                _overwrite_project(f, model.metadata.project)
            # create a project and add attributes
            project_group = self._get_or_create_group(
                f, model.metadata.project)
            project_attrs = model.metadata.__dict__
            project_attrs = {k: v for k,
                             v in project_attrs.items() if v is not None}

            project_group.attrs.update(project_attrs)

            # create a model group with input and output datasets
            model_group = self._get_or_create_group(
                project_group, model.version)

            if overwrite_datasets:
                _overwrite_datasets(model_group)

            if mode == 'python':
                # For the python option there is no need for an additional group
                _save_pickled(model_group, 'input', model)
                if result:
                    _save_pickled(model_group, 'output', result)

            if mode == 'json':
                raise NotImplementedError('JSON mode is not yet implemented')

            if mode == 'yaml':
                raise NotImplementedError('YAML mode is not yet implemented')

    def load(self, project: str, model: Optional[str] = None, load_results: bool = False, mode: Literal['python', 'json', 'yaml'] = 'python') -> Tuple[Model, Result]:
        """Load a single model or all models within a specific project."""

        def _load_pickled(group: h5py.Group, name: str, load_results: bool) -> Tuple[Model, Result]:
            pickle_in = group[name]['input'][()].tobytes()
            pickle_out = group[name]['output'][()].tobytes(
            ) if load_results else None

            model = pickle.loads(pickle_in)
            result = pickle.loads(pickle_out) if load_results else None
            return model, result

        with h5py.File(self.filename, 'r') as f:
            project_grp = f[project]

            if mode == 'python':
                if model is None:
                    all_models = list(project_grp.keys())
                    for item in all_models:
                        self.models[item] = _load_pickled(
                            group=project_grp, name=item, load_results=load_results)

                else:
                    self.models[model] = _load_pickled(
                        group=project_grp, name=model, load_results=load_results)

            if mode == 'json':
                raise NotImplementedError('JSON mode is not yet implemented')

            if mode == 'yaml':
                raise NotImplementedError('YAML mode is not yet implemented')


if __name__ == '__main__':
    from pyswap import testcase

    f = HDF5(filename='data.h5')

    # Create instances of the model and result
    model = testcase.get('hupselbrook')
    model2 = model.model_copy(
        update={'version': 'v2', 'crop': model.crop.model_copy(update={'rds': 195})})
    model3 = model.model_copy(
        update={'version': 'v3', 'crop': model.crop.model_copy(update={'rds': 100})})
    result = model.run('./')
    result2 = model.run('./')
    result3 = model.run('./')

    # Save to HDF5
    f.save_model(model=model, result=result,
                 overwrite_datasets=True, overwrite_project=True)
    f.save_model(model=model2, result=result2,
                 overwrite_datasets=True)
    f.save_model(model=model3, result=result3,
                 overwrite_datasets=True)

    # Load from HDF5
    f.load('pySWAP test - hupsel brook', load_results=True)

    print(f.models['base'][1].output[['TACT', 'TPOT']].resample('YE').sum())
    print(f.models['v2'][1].output[['TACT', 'TPOT']].resample('YE').sum())
    print(f.models['v3'][1].output[['TACT', 'TPOT']].resample('YE').sum())
