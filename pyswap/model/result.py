"""Capturing model results.

Tip:
    The Result class is now focusing on the output in CSV format and the log file. the other
    result files are also retrieved as a list of strings which user can access if needed.

Classes:
    Result: Stores the result of a model run.

"""
from pydantic import BaseModel, ConfigDict, computed_field, Field
from typing import Optional, List, Dict
from pandas import DataFrame
import re


class Result(BaseModel):
    """Class to store the result of a model run.

    Attributes:
        log (str): The log file of the model run.
        summary (str, optional): The summary file of the model run.
        output (DataFrame, optional): The output file of the model run.
        output_tz (DataFrame, optional): The output file of the model run with timezone.
        output_old (Dict[str, str], optional): The old output files of the model run.
        warning (List[str], optional): The warnings of the model run.
        model_config (ConfigDict): The configuration for the model.

    Methods:
        iteration_stats (str): The part of the log file that describes the iteration statistics.
        blc_summary (str): The .blc file if it exists.
        water_balance (str): The water balance of the model run.
    """

    log: str
    output: Optional[DataFrame] = Field(default=None, repr=False)
    output_tz: Optional[DataFrame] = Field(default=None, repr=False)
    output_old: Optional[Dict[str, str]] = Field(default=None, repr=False)
    warning: Optional[List[str]] = Field(default=None, repr=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra='forbid'
    )

    @computed_field(return_type=str)
    def iteration_stats(self):
        """Return the part of the string that describes the iteration statistics."""
        return re.search(r'.*(Iteration statistics\s*.*)$', self.log, re.DOTALL)[1]

    @computed_field(return_type=str)
    def blc_summary(self):
        """Return the .blc file if it exists."""
        return self.output_old.get('blc') if self.output_old else None

    def yearly_summary(self):
        """Return yearly sums of all output variables."""
        return self.output.resample('YE').sum()
