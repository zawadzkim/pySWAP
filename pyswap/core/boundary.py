from typing import Optional, Literal
from .utils.basemodel import PySWAPBaseModel
from .utils.fields import Table
from pydantic import model_validator, Field


class BottomBoundary(PySWAPBaseModel):

    swbbcfile: Literal[0, 1]
    swbotb: Literal[1, 2, 3, 4, 5, 6, 7, 8]
    bbcfile: Optional[str] = None
    # if swbotb == 1
    gwlevel: Optional[PySWAPBaseModel] = None
    # if swbotb == 2
    sw2: Literal[1, 2] = None
    # if sw2 == 1
    sinave: Optional[float] = Field(
        ge=-10.0, le=10.0, description='Average value of bottom flux [cm/d].', default=None)
    sinamp: Optional[float] = Field(
        ge=-10.0, le=10.0, description='Amplitude of bottom flux sine function [cm/d].', default=None)
    sinmax: Optional[float] = Field(
        ge=0.0, le=366.0, description='Time of the year with maximum bottom flux [d].', default=None)
    # if sw2 == 2
    table_qbot: Optional[Table] = None
    # if swbotb == 3
    swbotb3resvert: Optional[int] = None
    swbotb3impl: Optional[int] = None
    shape: Optional[float] = None
    hdrain: Optional[float] = None
    rimlay: Optional[float] = None
    sw3: Optional[int] = None
    # if sw3 == 1
    aquave: Optional[float] = None
    aquamp: Optional[float] = None
    aqtmax: Optional[float] = None
    aqtper: Optional[float] = None
    # if sw3 == 2
    table_haquif: Optional[Table] = None
    sw4: Optional[int] = None
    # if sw4 == 1
    table_qbot4: Optional[Table] = None
    # if swbotb == 4
    swqhbot: Optional[int] = None
    # if swqhbot == 1
    cofqha: Optional[float] = None
    cofqhb: Optional[float] = None
    cofqhc: Optional[float] = None
    # if swqhbot == 2
    table_qtab: Optional[Table] = None
    # if swbotb == 5
    table_hbot5: Optional[Table] = None

    @model_validator(mode='after')
    def _check_swbotb(self):
        if self.swbotb == 1:
            assert self.gwlevel, 'gwlevel must be provided if swbotb is 1'
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
                assert self.aquave, 'aquave must be provided if sw3 is 1'
                assert self.aquamp, 'aquamp must be provided if sw3 is 1'
                assert self.aqtmax, 'aqtmax must be provided if sw3 is 1'
                assert self.aqtper, 'aqtper must be provided if sw3 is 1'
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
