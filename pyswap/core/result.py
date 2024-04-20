"""Separate module for handling the output.

TODO: extract WARNINGS from log file and return them in a list
"""
from pydantic import BaseModel, ConfigDict, computed_field
from typing import Optional, Any, List
from pandas import DataFrame
import re


class Result(BaseModel):
    log: Optional[str]
    summary: Optional[str]
    output: Optional[DataFrame]
    vap: Optional[Any]
    warning: Optional[List[str]]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )

    @computed_field
    def iteration_stats(self):
        """Return the part of the string that describes the iteration statistics."""
        return re.search(r'.*(Iteration statistics\s*.*)$', self.log, re.DOTALL)[1]
