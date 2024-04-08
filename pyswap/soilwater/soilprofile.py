from ..core.utils.basemodel import PySWAPBaseModel
from ..core.utils.fields import Table
from pydantic import model_validator
from typing import Literal, Optional


class SoilProfile(PySWAPBaseModel):
    """Vertical discretization of soil profile, soil hydraulic functions and hysteresis of soil water retention."""
    table_soilprofile: Table
    swsophy: Literal[0, 1]
    swhyst: Literal[0, 1, 2]
    swmacro: Literal[0, 1]
    filenamesophy: Optional[str] = None
    tau: Optional[float] = None
    table_soilhydrfunc: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_soil_profile(self) -> None:

        if self.table_soilprofile is not None:
            required_columns_soil_profile = [
                "ISUBLAY", "ISOILLAY", "HSUBLAY", "HCOMP", "NCOMP"]
            for column in required_columns_soil_profile:
                assert column in self.table_soilprofile.columns, f"{column} is required in soilprofile"

        if self.swsophy == 0:
            required_columns_hydraulic_functions = [
                "ORES", "OSAT", "ALFA", "NPAR", "KSATFIT", "LEXP", "ALFAW", "H_ENPR", "KSATEXM", "BDENS"]
            assert self.table_soilhydrfunc is not None, "soilhydrfunc is required when swsophy is True"
            for column in required_columns_hydraulic_functions:
                assert column in self.table_soilhydrfunc.columns, f"{column} is required in soilhydrfunc"

        else:
            assert self.filenamesophy is not None, "filenamesophy is required when swsophy is True"

        if self.swhyst in range(1, 3):
            assert self.tau is not None, "tau is required when swhyst is 1 or 2"
