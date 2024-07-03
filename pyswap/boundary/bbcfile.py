"""
Bottom boundary condition settings for the SWAP model.

Classes:
    BottomBoundary: Holds the settings of the bottom boundary conditions of the .swp file.
"""

from typing import Optional, Literal
from typing_extensions import Self
from pydantic import model_validator, Field
from ..core import PySWAPBaseModel
from ..core import Table


class BBCFile(PySWAPBaseModel):
    """
    Bottom boundary settings for SWAP model.

    Attributes:
        swbotb (Literal[1, 2, 3, 4, 5, 6, 7, 8]): Switch for type of bottom boundary.

            * 1 - prescribe groundwater level;
            * 2 - prescribe bottom flux;
            * 3 - calculate bottom flux from hydraulic head of deep aquifer;
            * 4 - calculate bottom flux as function of groundwater level;
            * 5 - prescribe soil water pressure head of bottom compartment;
            * 6 - bottom flux equals zero;
            * 7 - free drainage of soil profile;
            * 8 - free outflow at soil-air interface.

        sw2 (Optional[Literal[1, 2]]): Specify whether a sinus function or a table are used for the bottom flux.

            * 1 - sinus function;
            * 2 - table.

        sw3 (Optional[Literal[1, 2]]): Specify whether a sinus function or a table are used for the hydraulic head in the deep aquifer.

            * 1 - sinus function;
            * 2 - table.

        sw4 (Optional[Literal[0, 1]]): An extra groundwater flux can be specified which is added to above specified flux.

            * 0 - no extra flux;
            * 1 - extra flux.

        swbotb3resvert (Optional[Literal[0, 1]]): Switch for vertical hydraulic resistance between bottom boundary and groundwater level.

            * 0 - Include vertical hydraulic resistance
            * 1 - Suppress vertical hydraulic resistance

        swbotb3impl (Optional[Literal[0, 1]]): Switch for numerical solution of bottom flux.

            * 0 - Explicit solution (choose always when SHAPE < 1.0);
            * 1 - Implicit solution.

        swqhbot (Optional[Literal[1, 2]]): Specify whether an exponential relation or a table is used.

            * 1 - bottom flux is calculated with an exponential relation
            * 2 - bottom flux is derived from a table

        bbcfile (Optional[str]): Name of file with bottom boundary data (without .BBC extension).
        sinave (Optional[float]): Average value of bottom flux.
        sinamp (Optional[float]): Amplitude of bottom flux sine function.
        sinmax (Optional[float]): Time of the year with maximum bottom flux.
        shape (Optional[float]): Shape factor to derive average groundwater level.
        hdrain (Optional[float]): Mean drain base to correct for average groundwater level.
        rimlay (Optional[float]): Vertical resistance of aquitard.
        aqave (Optional[float]): Average hydraulic head in underlaying aquifer.
        aqamp (Optional[float]): Amplitude hydraulic head sinus wave.
        aqtmax (Optional[float]): First time of the year with maximum hydraulic head.
        aqper (Optional[float]): Period of hydraulic head sinus wave.
        cofqha (Optional[float]): Coefficient A for exponential relation for bottom flux.
        cofqhb (Optional[float]): Coefficient B for exponential relation for bottom flux.
        cofqhc (Optional[float]): Coefficient C for exponential relation for bottom flux.
        gwlevel (Optional[Table]): Table with groundwater level data.
        table_qbot (Optional[Table]): Table with bottom flux data.
        table_haquif (Optional[Table]): Table with average pressure head in underlaying aquifer.
        table_qbot4 (Optional[Table]): Table with bottom flux data.
        table_qtab (Optional[Table]): Table with groundwater level-bottom flux relation
        table_hbot (Optional[Table]): Table with the bottom compartment pressure head.
    """

    swbotb: Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sw2: Optional[Literal[1, 2]] = Field(default=None)
    sw3: Optional[Literal[1, 2]] = Field(default=None)
    sw4: Optional[Literal[0, 1]] = Field(default=None)
    swbotb3resvert: Optional[Literal[0, 1]] = Field(default=None)
    swbotb3impl: Optional[Literal[0, 1]] = Field(default=None)
    swqhbot: Optional[Literal[1, 2]] = Field(default=None)
    sinave: Optional[float] = Field(
        ge=-10.0, le=10.0, default=None)
    sinamp: Optional[float] = Field(
        ge=-10.0, le=10.0, default=None)
    sinmax: Optional[float] = Field(
        ge=0.0, le=366.0, default=None)
    shape: Optional[float] = Field(default=None)
    hdrain: Optional[float] = Field(default=None)
    rimlay: Optional[float] = Field(default=None)
    aqave: Optional[float] = Field(default=None)
    aqamp: Optional[float] = Field(default=None)
    aqtmax: Optional[float] = Field(default=None)
    aqper: Optional[float] = Field(default=None)
    cofqha: Optional[float] = Field(default=None)
    cofqhb: Optional[float] = Field(default=None)
    cofqhc: Optional[float] = Field(default=None)
    table_gwlevel: Optional[Table] = Field(default=None)
    table_qbot: Optional[Table] = Field(default=None)
    table_haquif: Optional[Table] = Field(default=None)
    table_qbot4: Optional[Table] = Field(default=None)
    table_qtab: Optional[Table] = Field(default=None)
    table_hbot5: Optional[Table] = Field(default=None)

    @model_validator(mode='after')
    def _check_swbotb(self) -> Self:
        if self.swbotb == 1:
            assert not self.table_gwlevel.empty, 'table_gwlevel must be provided if swbotb is 1'
        elif self.swbotb == 2:
            assert self.sw2, 'sw2 must be provided if swbotb is 2'
            if self.sw2 == 1:
                assert self.sinave, 'sinave must be provided if sw2 is 1'
                assert self.sinamp, 'sinamp must be provided if sw2 is 1'
                assert self.sinmax, 'sinmax must be provided if sw2 is 1'
            elif self.sw2 == 2:
                assert self.table_qbot, 'qbot must be provided if sw2 is 2'
        elif self.swbotb == 3:
            assert self.sw3, 'sw3 must be provided if swbotb is 3'
            if self.sw3 == 1:
                assert self.aqave, 'aqave must be provided if sw3 is 1'
                assert self.aqamp, 'auamp must be provided if sw3 is 1'
                assert self.aqtmax, 'aqtmax must be provided if sw3 is 1'
                assert self.aqper, 'aqper must be provided if sw3 is 1'
            elif self.sw3 == 2:
                assert self.table_haquif, 'haquif must be provided if sw3 is 2'
        elif self.swbotb == 4:
            assert self.swqhbot, 'swqhbot must be provided if swbotb is 4'
            if self.swqhbot == 1:
                assert self.cofqha, 'cofqha must be provided if swqhbot is 1'
                assert self.cofqhb, 'cofqhb must be provided if swqhbot is 1'
                assert self.cofqhc, 'cofqhc must be provided if swqhbot is 1'
            elif self.swqhbot == 2:
                assert self.table_qtab, 'qtab must be provided if swqhbot is 2'
        elif self.swbotb == 5:
            assert self.table_hbot5, 'hbot5 must be provided if swbotb is 5'

        return self

    @property
    def content(self):
        return self._concat_sections()
