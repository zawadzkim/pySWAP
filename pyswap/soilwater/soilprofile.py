from typing import Literal, Self

from pydantic import model_validator

from ..core import PySWAPBaseModel, SerializableMixin, String, Table, YAMLValidatorMixin


class SoilProfile(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Vertical discretization of soil profile, soil hydraulic functions and
        hysteresis of soil water retention.

    Covers parts 4, 5, 6 and 7 of the .swp file.

    Attributes:
        swsophy (Literal[0, 1]): Switch for analytical functions or
            tabular input

            * 0 - Analytical functions with input of Mualem -
                van Genuchten parameters
            * 1 - Soil physical tables

        swhyst (Literal[0, 1, 2]): Hysteresis of soil water retention function

            * 0 - No hysteresis
            * 1 - Hysteresis, initial conditions wetting
            * 2 - Hysteresis, initial conditions drying

        filenamesophy (Optional[str]): Names of input files with
            soil hydraulic tables for each soil layer
        tau (Optional[float]): Minimum pressure head difference to change
            wetting-drying
        swmacro (Literal[0, 1]): Switch for preferential flow due to macropores
        table_soilprofile (Table): Table with soil profile data
        table_soilhydrfunc (Optional[Table]): Table with
            soil hydraulic functions
    """

    swsophy: Literal[0, 1]
    swhyst: Literal[0, 1, 2]
    swmacro: Literal[0, 1]
    filenamesophy: String | None = None
    tau: float | None = None
    table_soilprofile: Table
    table_soilhydrfunc: Table | None = None