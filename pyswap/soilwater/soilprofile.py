from ..core import PySWAPBaseModel
from ..core import Table
from pydantic import model_validator
from typing import Literal, Optional
from typing_extensions import Self


class SoilProfile(PySWAPBaseModel):
    """Vertical discretization of soil profile, soil hydraulic functions and hysteresis of soil water retention.

    Covers parts 4, 5, 6 and 7 of the .swp file.

    Attributes:
        swsophy (Literal[0, 1]): Switch for analytical functions or tabular input

            * 0 - Analytical functions with input of Mualem - van Genuchten parameters
            * 1 - Soil physical tables

        swhyst (Literal[0, 1, 2]): Hysteresis of soil water retention function

            * 0 - No hysteresis
            * 1 - Hysteresis, initial conditions wetting
            * 2 - Hysteresis, initial conditions drying

        filenamesophy (Optional[str]): Names of input files with soil hydraulic tables for each soil layer
        tau (Optional[float]): Minimum pressure head difference to change wetting-drying
        swmacro (Literal[0, 1]): Switch for preferential flow due to macropores
        table_soilprofile (Table): Table with soil profile data
        table_soilhydrfunc (Optional[Table]): Table with soil hydraulic functions
    """
    swsophy: Literal[0, 1]
    swhyst: Literal[0, 1, 2]
    swmacro: Literal[0, 1]
    filenamesophy: Optional[str] = None
    tau: Optional[float] = None
    table_soilprofile: Table
    table_soilhydrfunc: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_soil_profile(self) -> Self:

        if self.swsophy == 0:
            assert self.table_soilhydrfunc is not None, "table_soilhydrfunc is required when swsophy is True"
        else:
            assert self.filenamesophy is not None, "filenamesophy is required when swsophy is True"
        if self.swhyst in range(1, 3):
            assert self.tau is not None, "tau is required when swhyst is 1 or 2"

        return self
