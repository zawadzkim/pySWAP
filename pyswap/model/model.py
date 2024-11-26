"""The main model class.

Classes:
    Model: Main class that runs the SWAP model.
"""
from __future__ import annotations
import logging
import os
import shutil
import subprocess
import tempfile
import warnings
from importlib import resources
from pathlib import Path

from pandas import read_csv, to_datetime
from pydantic import Field, model_validator

from pyswap.components.boundary import BottomBoundary
from pyswap.components.crop import Crop
from pyswap.components.drainage import Drainage
from pyswap.components.irrigation import FixedIrrigation
from pyswap.components.meteorology import Meteorology
from pyswap.components.simsettings import GeneralSettings, RichardsSettings
from pyswap.components.soilwater import (
    Evaporation,
    SnowAndFrost,
    SoilMoisture,
    SoilProfile,
    SurfaceFlow,
)
from pyswap.components.transport import HeatFlow, SoluteTransport
from pyswap.core import IS_WINDOWS
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import ComplexSerializableMixin, FileMixin
from pyswap.libs import swap_linux, swap_windows
from pyswap.model.metadata import Metadata
from pyswap.model.result import Result

logger = logging.getLogger(__name__)
__all__ = ["Model"]


class ModelBuilder:
    """Class responsible for building the model components."""

    def __init__(self, model: Model):
        self.model = model

    def _write_swp(self, path: str) -> None:
        """Write the .swp input file."""
        self.model.save_file(string=self.model.swp, path=path, fname="swap", extension="swp")

    def _write_inputs(self, path: str) -> None:
        logger.info("Preparing files...")
        self._write_swp(path)
        if self.model.lateraldrainage.drafile:
            self.model.lateraldrainage.write_dra(path)
        if self.model.crop.cropfiles:
            self.model.crop.write_crop(path)
        if self.model.meteorology.metfile:
            self.model.meteorology.write_met(path)
        if self.model.fixedirrigation.irgfile:
            self.model.irrigation.fixedirrig.write_irg(path)
        if self.model.bottomboundary.swbbcfile:
            self.model.bottomboundary.write_bbc(path)


class ModelRunner:
    """Class responsible for running the model."""

    def __init__(self, model: Model):
        self.model = model

    @staticmethod
    def _copy_executable(tempdir: Path) -> None:
        """Copy the appropriate SWAP executable to the temporary directory."""
        if IS_WINDOWS:
            shutil.copy(swap_windows, tempdir)
            logger.info("Copying the windows version of SWAP into temporary directory...")
        else:
            shutil.copy(swap_linux, tempdir)
            logger.info("Copying linux executable into temporary directory...")

    @staticmethod
    def _run_swap(tempdir: Path) -> str:
        """Run the SWAP executable."""
        swap_path = Path(tempdir, "swap.exe") if IS_WINDOWS else "./swap420"
        p = subprocess.Popen(
            swap_path,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=tempdir,
        )
        stdout = p.communicate(input=b"\n")[0]
        return stdout.decode()

    def _raise_swap_warning(self, message):
        warnings.warn(message, Warning, stacklevel=3)

    def run(self, path: str | Path, silence_warnings: bool = False, old_output: bool = True):
        """Main function that runs the model."""
        with tempfile.TemporaryDirectory(dir=path) as tempdir:

            self._copy_executable(tempdir)
            ModelBuilder(self.model)._write_inputs(tempdir)
            result = self._run_swap(tempdir)

            if "normal completion" not in result:
                raise Exception(f"Model run failed. \n {result}")
            
            logger.info(result)

            r = ResultReader()

            log = r._read_log_file(tempdir)
            warnings = r._identify_warnings(log)

            output = None
            output_tz = None

            if 'csv' in self.model.general_settings.extensions:
                output_path = Path(tempdir, f"{self.model.general_settings.outfil}_output.csv")
                if output_path.exists():
                    output = r._read_output(output_path)
                else:
                    logger.warning(f"Expected output file {output_path} not found.")

            if 'csv_tz' in self.model.general_settings.extensions:
                output_tz_path = Path(tempdir, f"{self.model.general_settings.outfil}_output_tz.csv")
                if output_tz_path.exists():
                    output_tz = r._read_output_tz(output_tz_path)
                else:
                    logger.warning(f"Expected output_tz file {output_tz_path} not found.")

            if warnings and not silence_warnings:
                logger.warning("Warnings:")
                for warning in warnings:
                    self._raise_swap_warning(message=warning)
                    
            dict_files = r._read_output_old(self.model, tempdir) if old_output else None
            
            result = Result(
                output=output,
                output_tz=output_tz,
                log=log,
                output_old=dict_files,
                warning=warnings,
            )
            return result

class ResultReader:
    """Class responsible for reading the model results."""

    @staticmethod
    def _read_output(path: Path):
        """Read the output csv file."""
        df = read_csv(path, comment="*", index_col="DATETIME")
        df.index = to_datetime(df.index)
        return df

    @staticmethod
    def _read_output_tz(path: Path):
        """Read the output csv file with the depth information."""
        df = read_csv(path, comment="*", index_col="DATE")
        df.index = to_datetime(df.index)
        return df

    def _read_log_file(self, directory: Path) -> str:
        """Read the log file."""

        log_files = [f for f in Path(directory).glob("*.log") if f.name != "reruns.log"]

        if len(log_files) == 0:
            msg = "No .log file found in the directory."
            raise FileNotFoundError(msg)
        elif len(log_files) > 1:
            msg = "Multiple .log files found in the directory."
            raise FileExistsError(msg)
        
        log_file = log_files[0]

        with open(log_file) as file:
            log_content = file.read()

        return log_content

    @staticmethod
    def _identify_warnings(log: str) -> list[Warning]:
        """Read through the log file and catch warnings emitted by the SWAP executable."""
        lines = log.split("\n")
        warnings = [line for line in lines if line.strip().lower().startswith("warning")]
        return warnings

    def _read_output_old(self, model: Model, tempdir: Path):
        """Read all output files that are not in csv format as strings."""
        list_dir = os.listdir(tempdir)
        list_dir = [
            f for f in list_dir if not f.find(model.general_settings.outfil) and not f.endswith(".csv")
        ]
        if list_dir:
            dict_files = {
                f.split(".")[1]: model.read_file(Path(tempdir, f)) for f in list_dir
            }
        return dict_files


class Model(PySWAPBaseModel, FileMixin, ComplexSerializableMixin):
    """Main class that runs the SWAP model.

    Attributes:
        metadata (Any): Metadata of the model.
        general_settings (Any): Simulation settings.
        meteorology (Any): Meteorological data.
        crop (Any): Crop data.
        fixedirrigation (Any): Fixed irrigation settings.
        soilmoisture (Any): Soil moisture data.
        surfaceflow (Any): Surface flow data.
        evaporation (Any): Evaporation data.
        soilprofile (Any): Soil profile data.
        snowandfrost (Optional[Any]): Snow and frost data.
            Default is `SnowAndFrost(swsnow=0, swfrost=0)`.
        richards (Optional[Any): Richards data.
        lateraldrainage (Any): Lateral drainage data.
        bottomboundary (Any): Bottom boundary data.
        heatflow (Optional[Any): Heat flow data.
        solutetransport (Optional[Any): Solute transport data.

    Methods:
        write_swp: Write the .swp input file.
        _copy_executable: Copy the appropriate SWAP executable to
            the temporary directory.
        _run_swap: Run the SWAP executable.
        _read_output: Read the output file.
        _read_output_tz: Read the output file with time zone.
        _read_vap: Read the .vap output file.
        _write_inputs: Write the input files.
        _identify_warnings: Identify warnings in the log file.
        _raise_swap_warning: Raise a warning.
        _read_output_old: Save the old output files.
        run: Run the model.
    """

    _validate_on_run: bool = False
    _use_comp_dict: bool = False

    metadata: Metadata | None = None
    version: str = Field(exclude=True, default="base")
    general_settings: GeneralSettings | None = None
    meteorology: Meteorology | None = None
    crop: Crop | None = None
    fixedirrigation: FixedIrrigation | None = FixedIrrigation(swirfix=0)
    soilmoisture: SoilMoisture | None = None
    surfaceflow: SurfaceFlow | None = None
    evaporation: Evaporation | None = None
    soilprofile: SoilProfile | None = None
    snowandfrost: SnowAndFrost | None = SnowAndFrost(swsnow=0, swfrost=0)
    richards: RichardsSettings | None = RichardsSettings(swkmean=1, swkimpl=0)
    lateraldrainage: Drainage | None = None
    bottomboundary: BottomBoundary | None = None
    heatflow: HeatFlow | None = HeatFlow(swhea=0)
    solutetransport: SoluteTransport | None = SoluteTransport(swsolu=0)
    comp: dict = Field(default_factory=dict, exclude=True)

    @property
    def components(self):
        """Return the components of the model already added to the model."""
        return self.comp.keys()
    
    def get_component(self, component: str, copy: bool = False):
        """Get a model component (section) from dictionary.

        Parameters:
            component (str): Name of the component (section) to get.
            copy (bool): Whether to return a copy of the component.

        Returns:
            PySWAPBaseModel: The model component.
        """

        if copy:
            return self.comp.get(component.lower()).model_copy(deep=True)
        else:
            return self.comp.get(component.lower())

    def set_component(self, component: PySWAPBaseModel, replace: bool = True):
        """Add or replace a model component (section) in dictionary.

        Got this from Pastas.

        Parameters:
            component (PySWAPBaseModel): component (section) of SWAP model.
            replace (bool): Whether to replace the section if one of the same
                name is already in the dictionary.
        """
        
        if isinstance(component, list):
            for comp in component:
                self.set_component(comp)

        elif (component.name in self.comp.keys()) and not replace:
            message = (
                "The component with the same name already exists "
                "in this model. Set replace to True if you want to "
                "replace it with a new one."
            )
            logger.warning(message)
            return None

        else:
            if component.name in self.comp.keys():
                logger.warning(
                    "The component with the same name already exists "
                    "in this model. The component is replaced."
                )

            self.comp[component.name] = component

    def remove_component(self, component: str):
        """Remove a component from the dictionary.
        
        Parameters:
            component (str): Name of the component to remove,
                case-insensitive, corresponds to pySWAP class name.
        """
        if component not in self.comp:
            raise KeyError(f"Component '{component}' not found.")
        self.comp.pop(component)


    @model_validator(mode='after')
    def validate_all_components(self):
        if not getattr(self, '_validate_on_run', False):
            return self

        required_components = [
            "metadata", "generalsettings", "meteorology", "crop", "fixedirrigation",
            "soilmoisture", "surfaceflow", "evaporation", "soilprofile", "snowandfrost",
            "richards", "lateraldrainage", "bottomboundary", "heatflow", "solutetransport"
        ]
        missing_components = [comp for comp in required_components if comp not in self.comp]
        if missing_components:
            raise ValueError(f"Missing required components: {', '.join(missing_components)}")
        return self

    def validate(self):
        try:
            self._validate_on_run = True
            self.model_validate(self, context={'_validate_on_run': True})
        finally:
            self._validate_on_run = False
            logger.info("Validation successful.")

    @property
    def swp(self):
        """The content of the swp file.

        Looping over the dict() because when model_dump() is
        used, the nested models are automatically serialized.
        """
        return self.concat_nested_models(self)

    def run(self, path: str | Path, silence_warnings: bool = False, old_output: bool = True):
        """Run the model using ModelRunner."""
        if self.comp:
            self.validate()
        return ModelRunner(self).run(path, silence_warnings, old_output)
