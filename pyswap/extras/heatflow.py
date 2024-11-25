"""Heat flow settings for SWAP simulation.

Classes:
    HeatFlow: Heat flow settings for SWAP simulation.
"""

from typing import Literal, Self

from pydantic import model_validator

from ..core import PySWAPBaseModel, SerializableMixin, String, Table
from ..core.mixins import YAMLValidatorMixin


class HeatFlow(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Heat flow settings for SWAP simulation.

    !!! warning

        table_initsoil is not validated because it depends of swinco setting.

    Attributes:
        swhea (Literal[0, 1]): Switch for heat flow.
        swcalt (Optional[Literal[1, 2]]):

            * 1 - analytical method
            * 2 - numerical method

        tampli (Optional[float]): Amplitude of annual temperature wave atsoil
            surface [0..50 oC, R]
        tmean (Optional[float]): Mean annual temperature at
            soil surface[-10..30 oC, R]
        timref (Optional[float]): Time at which the sinus temperature
            wave reaches it's top [0..366.0 d, R]
        ddamp (Optional[float]): Damping depth of soil temperature
            wave[1..500 cm, R]
        swtopbhea (Optional[Literal[1, 2]]): Define top boundary condition

            * 1 - use air temperature of meteo input file as top boundary
            * 2 - use measured top soil temperature as top boundary

        tsoilfile (Optional[str]): name of input file with soil
            surface temperatures without extension .TSS
        swbotbhea (Optional[Literal[1, 2]]): Define bottom boundary condition

            * 1 - no heat flux
            * 2 - prescribe bottom temperature

        table_soiltextures (Optional[Table]): for each physical
            soil layer the soil texture (g/g mineral parts) and the
            organic matter content (g/g dry soil)
        table_initsoil (Optional[Table]): initial temperature TSOIL
            [-50..50 oC, R] as function of soil depth ZH [-100000..0 cm, R]
        table_bbctsoil (Optional[Table]): bottom boundary temperature TBOT
            [-50..50 oC, R] as function of date DATET [date]
    """

    swhea: Literal[0, 1]
    swcalt: Literal[1, 2] | None = None
    tampli: float | None = None
    tmean: float | None = None
    timref: float | None = None
    ddamp: float | None = None
    swtopbhea: Literal[1, 2] | None = None
    tsoilfile: String | None = None
    swbotbhea: Literal[1, 2] | None = None
    table_soiltextures: Table | None = None
    table_initsoil: Table | None = None
    table_bbctsoil: Table | None = None
