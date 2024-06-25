"""Heat flow settings for SWAP simulation.

Classes:
    HeatFlow: Heat flow settings for SWAP simulation.
"""
from ..core import PySWAPBaseModel
from ..core import Table
from typing import Literal, Optional
from typing_extensions import Self
from pydantic import model_validator


class HeatFlow(PySWAPBaseModel):
    """Heat flow settings for SWAP simulation.

    !!! warning

        table_initsoil is not validated because it depends of swinco setting.

    Attributes:
        swhea (Literal[0, 1]): Switch for heat flow.
        swcalt (Optional[Literal[1, 2]]):

            * 1 - analytical method
            * 2 - numerical method

        tampli (Optional[float]): Amplitude of annual temperature wave at soil surface [0..50 oC, R]
        tmean (Optional[float]): Mean annual temperature at soil surface [-10..30 oC, R]
        timref (Optional[float]): Time at which the sinus temperature wave reaches it's top [0..366.0 d, R]
        ddamp (Optional[float]): Damping depth of soil temperature wave [1..500 cm, R]
        swtopbhea (Optional[Literal[1, 2]]): Define top boundary condition

            * 1 - use air temperature of meteo input file as top boundary
            * 2 - use measured top soil temperature as top boundary

        tsoilfile (Optional[str]): name of input file with soil surface temperatures without extension .TSS
        swbotbhea (Optional[Literal[1, 2]]): Define bottom boundary condition

            * 1 - no heat flux
            * 2 - prescribe bottom temperature

        table_soiltextures (Optional[Table]): for each physical soil layer the soil texture (g/g mineral parts) and the organic matter content (g/g dry soil)
        table_initsoil (Optional[Table]): initial temperature TSOIL [-50..50 oC, R] as function of soil depth ZH [-100000..0 cm, R]
        table_bbctsoil (Optional[Table]): bottom boundary temperature TBOT [-50..50 oC, R] as function of date DATET [date]
    """

    swhea: Literal[0, 1]
    swcalt: Optional[Literal[1, 2]] = None
    tampli: Optional[float] = None
    tmean: Optional[float] = None
    timref: Optional[float] = None
    ddamp: Optional[float] = None
    swtopbhea: Optional[Literal[1, 2]] = None
    tsoilfile: Optional[str] = None
    swbotbhea: Optional[Literal[1, 2]] = None
    table_soiltextures: Optional[Table] = None
    table_initsoil: Optional[Table] = None
    table_bbctsoil: Optional[Table] = None

    @model_validator(mode='after')
    def _check_heatflow(self) -> Self:
        if self.swhea == 1:
            assert self.swcalt is not None, "swcalt must be specified if swhea is 1"
            if self.swcalt == 1:
                assert self.tampli is not None, "tampli must be specified if swcalt is 1"
                assert self.tmean is not None, "tmean must be specified if swcalt is 1"
                assert self.timref is not None, "timref must be specified if swcalt is 1"
                assert self.ddamp is not None, "ddamp must be specified if swcalt is 1"
            elif self.swcalt == 2:
                assert self.table_soiltextures is not None, "table_soiltextures must be specified if swcalt is 2"
                if self.swtopbhea == 2:
                    assert self.tsoilfile is not None, "tsoilfile must be specified if swtopbhea is 2"
                if self.swbotbhea == 2:
                    assert self.table_bbctsoil is not None, "table_bbctsoil must be specified if swbotbhea is 2"
        return self
