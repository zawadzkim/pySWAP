from dataclasses import dataclass, field
from ..core.utils.basemodel import Section, Subsection, PySWAPBaseModel
from pandas import DataFrame
from pydantic import model_validator
from typing import Literal, Optional


class SoilProfile(PySWAPBaseModel):
    """Vertical discretization of soil profile, soil hydraulic functions and hysteresis of soil water retention."""
    soilprofile: DataFrame
    swsophy: bool
    swhyst: Literal[0, 1, 2]
    swmacro: bool
    filenamesophy: Optional[str] = None,
    tau: Optional[float] = None
    soilhydrfunc: Optional[DataFrame] = None

    @model_validator(mode='after')
    def _validate_soil_profile(self) -> None:

        if self.soilprofile is not None:
            required_columns_soil_profile = [
                "ISUBLAY", "ISOILLAY", "HSUBLAY", "HCOMP", "NCOMP"]
            for column in required_columns_soil_profile:
                assert column in self.soilprofile.columns, f"{column} is required in soilprofile"

        if self.swsophy:
            required_columns_hydraulic_functions = [
                "ORES", "OSAT", "ALFA", "NPAR", "KSATFIT", "LEXP", "ALFAW", "H_ENPR", "KSATEXM", "BDENS"]
            assert self.soilhydrfunc is not None, "soilhydrfunc is required when swsophy is True"
            for column in required_columns_hydraulic_functions:
                assert column in self.soilhydrfunc.columns, f"{column} is required in soilhydrfunc"

        else:
            assert self.filenamesophy is not None, "filenamesophy is required when swsophy is True"

        if self.swhyst in range(1, 3):
            assert self.tau is not None, "tau is required when swhyst is 1 or 2"
