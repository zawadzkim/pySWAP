from typing import Literal, Self

from ..core import PySWAPBaseModel, SerializableMixin, String, Table, YAMLValidatorMixin


class SoilMoisture(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Soil moisture content and water balance.

    !!! warning
        swinco = 3 is not yet implemented. The model will run, but the output
        will not be retrieved.

    Attributes:
        swinco (int): Switch for the type of initial soil moisture condition:

            * 1 - pressure head as function of soil depth.
            * 2 - pressure head of each compartment is in
                hydrostatic equilibrium with initial groundwater level.
            * 3 - read final pressure heads from output file of previous
                Swap simulation.

        table_head_soildepth (Optional[Table]): Table with head and
            soil depth data.
        gwli (Optional[float]): Initial groundwater level [cm].
        inifil (Optional[str]): name of output file *.END which contains
            initial values.
    """

    swinco: Literal[1, 2, 3]
    table_head_soildepth: Table | None = None
    gwli: float | None = None
    inifil: String | None = None
