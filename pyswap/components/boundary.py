from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String, Table
from pyswap.core.mixins import YAMLValidatorMixin, FileMixin, SerializableMixin


from pydantic import Field, field_validator, model_validator


from decimal import Decimal
from typing import Literal, Self

__all__ = ["BottomBoundary", "BBCFile"]


class BottomBoundaryBase(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """
    Bottom boundary settings for SWAP model.

    Attributes:
        swbotb (Literal[1, 2, 3, 4, 5, 6, 7, 8]): Switch for type of
            bottom boundary.

            * 1 - prescribe groundwater level;
            * 2 - prescribe bottom flux;
            * 3 - calculate bottom flux from hydraulic head of deep aquifer;
            * 4 - calculate bottom flux as function of groundwater level;
            * 5 - prescribe soil water pressure head of bottom compartment;
            * 6 - bottom flux equals zero;
            * 7 - free drainage of soil profile;
            * 8 - free outflow at soil-air interface.

        sw2 (Optional[Literal[1, 2]]): Specify whether a sinus function or
            a table are used for the bottom flux.

            * 1 - sinus function;
            * 2 - table.

        sw3 (Optional[Literal[1, 2]]): Specify whether a sinus function or
            a table are used for the hydraulic head in the deep aquifer.

            * 1 - sinus function;
            * 2 - table.

        sw4 (Optional[Literal[0, 1]]): An extra groundwater flux can be
            specified which is added to above specified flux.

            * 0 - no extra flux;
            * 1 - extra flux.

        swbotb3resvert (Optional[Literal[0, 1]]): Switch for vertical
            hydraulic resistance between bottom boundary and groundwater level.

            * 0 - Include vertical hydraulic resistance
            * 1 - Suppress vertical hydraulic resistance

        swbotb3impl (Optional[Literal[0, 1]]): Switch for numerical solution
            of bottom flux.

            * 0 - Explicit solution (choose always when SHAPE < 1.0);
            * 1 - Implicit solution.

        swqhbot (Optional[Literal[1, 2]]): Specify whether an exponential
            relation or a table is used.

            * 1 - bottom flux is calculated with an exponential relation
            * 2 - bottom flux is derived from a table

        bbcfile (Optional[str]): Name of file with bottom boundary data
            (without .BBC extension).
        sinave (Optional[Decimal]): Average value of bottom flux.
        sinamp (Optional[Decimal]): Amplitude of bottom flux sine function.
        sinmax (Optional[Decimal]): Time of the year with maximum bottom flux.
        shape (Optional[Decimal]): Shape factor to derive average groundwater
            level.
        hdrain (Optional[Decimal]): Mean drain base to correct for average
            groundwater level.
        rimlay (Optional[Decimal]): Vertical resistance of aquitard.
        aqave (Optional[Decimal]): Average hydraulic head in underlaying
            aquifer.
        aqamp (Optional[Decimal]): Amplitude hydraulic head sinus wave.
        aqtmax (Optional[Decimal]): First time of the year with maximum
            hydraulic head.
        aqper (Optional[Decimal]): Period of hydraulic head sinus wave.
        cofqha (Optional[Decimal]): Coefficient A for exponential relation for
            bottom flux.
        cofqhb (Optional[Decimal]): Coefficient B for exponential relation for
            bottom flux.
        cofqhc (Optional[Decimal]): Coefficient C for exponential relation for
            bottom flux.
        gwlevel (Optional[Table]): Table with groundwater level data.
        table_qbot (Optional[Table]): Table with bottom flux data.
        table_haquif (Optional[Table]): Table with average pressure head in
            underlaying aquifer.
        table_qbot4 (Optional[Table]): Table with bottom flux data.
        table_qtab (Optional[Table]): Table with groundwater level-bottom
            flux relation
        table_hbot (Optional[Table]): Table with the bottom compartment
            pressure head.
    """

    swbotb: Literal[1, 2, 3, 4, 5, 6, 7, 8] | None = None
    sw2: Literal[1, 2] | None = None
    sw3: Literal[1, 2] | None = None
    sw4: Literal[0, 1] | None = None
    swbotb3resvert: Literal[0, 1] | None = None
    swbotb3impl: Literal[0, 1] | None = None
    swqhbot: Literal[1, 2] | None = None
    bbcfil: String | None = None
    sinave: Decimal | None = Field(ge=-10.0, le=10.0, default=None)
    sinamp: Decimal | None = Field(ge=-10.0, le=10.0, default=None)
    sinmax: Decimal | None = Field(ge=0.0, le=366.0, default=None)
    shape: Decimal | None = None
    hdrain: Decimal | None = None
    rimlay: Decimal | None = None
    aqave: Decimal | None = None
    aqamp: Decimal | None = None
    aqtmax: Decimal | None = None
    aqper: Decimal | None = None
    cofqha: Decimal | None = None
    cofqhb: Decimal | None = None
    cofqhc: Decimal | None = None
    table_gwlevel: Table | None = None
    table_qbot: Table | None = None
    table_haquif: Table | None = None
    table_qbot4: Table | None = None
    table_qtab: Table | None = None
    table_hbot5: Table | None = None

    @model_validator(mode="after")
    def _check_swbotb(self) -> Self:
        if self.swbotb == 1:
            assert self.table_gwlevel is not None and not self.table_gwlevel.empty, (
                "table_gwlevel must be provided if swbotb is 1"
            )
        elif self.swbotb == 2:
            assert self.sw2, "sw2 must be provided if swbotb is 2"
            if self.sw2 == 1:
                assert self.sinave, "sinave must be provided if sw2 is 1"
                assert self.sinamp, "sinamp must be provided if sw2 is 1"
                assert self.sinmax, "sinmax must be provided if sw2 is 1"
            elif self.sw2 == 2:
                assert self.table_qbot is not None and not self.table_qbot.empty, (
                    "qbot must be provided if sw2 is 2"
                )
        elif self.swbotb == 3:
            assert self.sw3, "sw3 must be provided if swbotb is 3"
            if self.sw3 == 1:
                assert self.aqave, "aqave must be provided if sw3 is 1"
                assert self.aqamp, "auamp must be provided if sw3 is 1"
                assert self.aqtmax, "aqtmax must be provided if sw3 is 1"
                assert self.aqper, "aqper must be provided if sw3 is 1"
            elif self.sw3 == 2:
                assert self.table_haquif is not None and not self.table_haquif.empty, (
                    "haquif must be provided if sw3 is 2"
                )
        elif self.swbotb == 4:
            assert self.swqhbot, "swqhbot must be provided if swbotb is 4"
            if self.swqhbot == 1:
                assert self.cofqha, "cofqha must be provided if swqhbot is 1"
                assert self.cofqhb, "cofqhb must be provided if swqhbot is 1"
                assert self.cofqhc, "cofqhc must be provided if swqhbot is 1"
            elif self.swqhbot == 2:
                assert self.table_qtab is not None and self.table_qtab.empty, (
                    "qtab must be provided if swqhbot is 2"
                )
        elif self.swbotb == 5:
            assert self.table_hbot5 is not None and self.table_hbot5.empty, (
                "hbot5 must be provided if swbotb is 5"
            )

        return self

    @field_validator(
        "sinave",
        "sinamp",
        "sinmax",
        "shape",
        "hdrain",
        "rimlay",
        "aqave",
        "aqamp",
        "aqtmax",
        "aqper",
        "cofqha",
        "cofqhb",
        "cofqhc",
    )
    def set_decimals(cls, v):
        return v.quantize(Decimal("0.00"))


class BBCFile(BottomBoundaryBase, FileMixin):
    """Bottom boundary file.

    All attributes are the same as in the BottomBOundaryBase. There
    is an additional property allowing to save the content to a file.
    """


class BottomBoundary(BottomBoundaryBase):
    """Bottom boundary condition settings in the swp file.

    Attributes:
        swbbcfile (Literal[0, 1]): Switch for file with bottom boundary data:

            * 0 - data are specified in current file
            * 1 - data are specified in separate file


        bbcfile (Optional[BBCFile]): the BBCFile object.
    """

    swbbcfile: Literal[0, 1]
    bbcfile: BBCFile | None = None

    @property
    def bbc(self):
        return "".join(self.bbcfile.concat_attributes())

    def write_bbc(self, path: str):
        self.bbcfile.save_file(
            string=self.bbc, extension="bbc", fname=self.bbcfil, path=path
        )