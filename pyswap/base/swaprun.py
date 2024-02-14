"""
This module contains the SwapRun class which is used to run the SWAP model.
"""
import os
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from .result import SWAPResult
from .swpsetup import SWAPSetup
from pySWAP.utils_database.models import SWAPModel, ModelIteration, ModelOutput
from pySWAP.utils_database.connection import DatabaseConnection
from sqlalchemy.orm.exc import NoResultFound


@dataclass
class SWAPRun:
    model: SWAPSetup | None = None
    model_base = None  # the whole row of the model in the database
    model_iteration = None  # the whole row of the model in the database
    iteration_change: dict | None = None
    new_swp: dict | None = None
    new_crop = None
    new_drainage = None
    new_met = None
    result: SWAPResult = None

    def get_model_by_name(self):
        try:
            self.model_base = self.model.connection.session.query(SWAPModel).\
                filter_by(name=self.model.metadata.project_name).first()

        except NoResultFound:
            self.model_base = None
        try:
            # get the latest iteration for the current model:
            self.model_iteration = self.model.connection.session.query(ModelIteration).\
                filter_by(model_id=self.model_base.id).\
                order_by(ModelIteration.iteration.desc()).first()

        except NoResultFound:
            self.model_iteration = None

    def include_iteration_changes(self):
        """Merge the base model with the iteration changes"""

        if self.model_iteration is not None:
            self.model_base.swp.update(self.model_iteration.swp_change)
            self.model_base.drainage.update(self.model_iteration.drainage_change)
            self.model_base.crop.update(self.model_iteration.crop_change)

            self.new_swp = self.model_base.swp
            self.new_drainage = self.model_base.drainage
            self.new_crop = self.model_base.crop

    def pop_nons(self):
        """Remove all parameters that have a None value inside each nested dictionary"""

        if self.new_swp is not None:
            for key in list(self.new_swp.keys()):  # list is needed to avoid RuntimeError
                self.new_swp[key] = {k: v for k, v in self.new_swp[key].items() if v is not None}

    def bool_to_int(self):
        """Convert all boolean values to integers inside each nested dictionary"""

        if self.new_swp is not None:
            for key in list(self.new_swp.keys()):
                self.new_swp[key] = {k: int(v) if isinstance(v, bool) else v for k, v in
                                           self.new_swp[key].items()}

    # decode the meteo data from the feather file in the database
    def decode_meteo(self):
        import pandas as pd
        import pyarrow.feather as feather
        import io
        import base64

        if self.model_base.met is not None:
            meteo = feather.read_feather(io.BytesIO(self.model_base.met))
            self.new_met = meteo

    def compile_swp_file(self):

        file_text: str = ''

        if self.new_swp is not None:
            for item, value in self.new_swp.items():

                for param, param_value in self.new_swp[item].items():

                    if not param.startswith('TABLE_'):
                        if isinstance(param_value, str) and not param_value[0].isdigit():
                            param_value = f"'{param_value}'"
                        file_text += f"{param} = {param_value} \n"
                    else:
                        file_text += f"{param_value} \n"

        return file_text

    def store_results(self, directory: str, iteration_id: int):
        # Loop through all files in the directory
        for file_name in os.listdir(directory):
            # Check if the file starts with 'result'
            if file_name.startswith('result'):
                # Get the file extension
                file_type = os.path.splitext(file_name)[1][1:]
                # Read the file in binary format
                with open(os.path.join(directory, file_name), 'rb') as file:
                    data = file.read()
                # Create an instance of the ModelOutput model
                output = ModelOutput(iteration_id=iteration_id, file_name=file_name,
                                     file_type=file_type, data=data)
                # Add the instance to the session
                try:
                    self.model.connection.session.add(output)
                    self.model.connection.session.commit()
                except IntegrityError:
                    self.model.connection.session.rollback()


    def run(self):

        import shutil
        import tempfile
        import subprocess
        from pySWAP.utils.utils import save_file

        # sanitize the swp file
        self.pop_nons()
        self.bool_to_int()
        self.decode_meteo()
        # test_directory = r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\testing"

        # Create a temporary directory in memory
        with tempfile.TemporaryDirectory(dir=r'../') as tempdir:
            # Copy existing files into the temporary directory
            exe_file_path = r'data\.exe\swap.exe'
            print('Copying files into temporary directory...')
            # shutil.copy(r'..\data\283.met', tempdir)
            # Saving met file
            save_file(string=self.new_met.to_csv(index=False, lineterminator='\n'),
                      extension='met',
                      fname=f'meteo_{self.model.meteo.station}',
                      path=tempdir,
                      mode='w')

            # Saving dra file
            save_file(string=self.new_drainage['swap'],
                      extension='dra',
                      fname='swap',
                      path=tempdir,
                      mode='w')
            # save crop files
            for key, value in self.new_crop.items():
                save_file(string=value,
                          extension='crp',
                          fname=key,
                          path=tempdir,
                          mode='w',
                          encoding='ascii')
            # save swp file
            save_file(string=self.compile_swp_file(),
                      extension='swp',
                      fname='swap',
                      path=tempdir,
                      mode='w',
                      encoding='ascii')
            # keep the temporary directory for debugging purposes

            print('Copying executable into temporary directory...')
            shutil.copy(exe_file_path, tempdir)

            # shutil.copytree(tempdir, test_directory)
            print('Running SWAP...')
            # Run the exe file as subprocess and capture the output
            result = subprocess.run([os.path.join(tempdir, 'swap.exe')],
                                    stdout=subprocess.PIPE,
                                    cwd=tempdir)

            # Print the output to the console
            print(result.stdout.decode())

            log_file = os.path.join(tempdir, 'swap_swap.log')
            self.store_results(tempdir, self.model_iteration.id)
            # Read the log file produced by the exe file
            with open(log_file, 'r') as f:
                log_data = f.read()
                print(log_data)

            # keep the temporary directory for debugging purposes
            # shutil.copytree(tempdir, r"C:\Users\zawad\PycharmProjects\pySWAP_django\djangoSWAP\setup_model\pySWAP\pySWAP\data\testing")


