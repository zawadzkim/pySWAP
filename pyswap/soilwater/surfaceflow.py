from typing import Literal, Self

from pydantic import model_validator

from ..core import PySWAPBaseModel, SerializableMixin, String, Table, YAMLValidatorMixin


class SurfaceFlow(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Surface flow settings (ponding, runoff and runon).

    Attributes:
        swpondmx (Literal[0, 1]): Switch for variation ponding
            threshold for runoff

            * 0 - Ponding threshold for runoff is constant
            * 1 - Ponding threshold for runoff varies in time

        swrunon (Literal[0, 1]): Switch for runon

            * 0 - No runon
            * 1 - Use runon data

        rsro (float): Drainage resistance for surface runoff
        rsroexp (float): Exponent for drainage equation of surface runoff
        pondmx (Optional[float]): In case of ponding, minimum
            thickness for runoff
        rufil (Optional[str]): Name of the runon file
        table_pondmxtb (Optional[Table]): Minimum thickness for runoff as
            a function of time
    """

    swpondmx: Literal[0, 1]
    swrunon: Literal[0, 1]
    rsro: float = 0.5
    rsroexp: float = 1.0
    pondmx: float | None = None
    rufil: String | None = None
    table_pondmxtb: Table | None = None
