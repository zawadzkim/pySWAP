"""Capturing model results.

Tip:
    The Result class is now focusing on the output in CSV format and the log file. the other
    result files are also retrieved as a list of strings which user can access if needed.

Classes:
    Result: Stores the result of a model run.

"""

import re

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field, computed_field

__all__ = ["Result"]


class Result(BaseModel):
    """Class to store the result of a model run.

    Attributes:
        log (str): The log file of the model run.
        output (DataFrame, optional): The output file of the model run.
        warning (List[str], optional): The warnings of the model run.

    Properties:
        model_config (dict): The model configuration.
        ascii (dict): The output in ASCII format.
        csv (DataFrame): The output in CSV format.
        iteration_stats (str): The part of the log file that describes the iteration statistics.
        blc_summary (str): The .blc file if it exists.
        yearly_summary (DataFrame): Yearly sums of all output variables.
    """

    log: str | None = Field(default=None, repr=False)
    output: dict | None = Field(default_factory=dict, repr=False)
    warning: list[str] | None = Field(default=None, repr=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    @computed_field(return_type=dict)
    def ascii(self):
        """Return the output in ASCII format."""
        return {k: v for k, v in self.output.items() if not k.endswith("csv")}

    @computed_field(return_type=DataFrame)
    def csv(self):
        """Return the output in CSV format."""
        return self.output.get("csv", None)
    
    @computed_field(return_type=DataFrame)
    def csv_tz(self):
        """Return the output in CSV format with depth."""
        return self.output.get("csv_tz", None)

    @computed_field(return_type=str)
    def iteration_stats(self):
        """Return the part of the string that describes the iteration statistics."""
        return re.search(r".*(Iteration statistics\s*.*)$", self.log, re.DOTALL)[1]

    @computed_field(return_type=str)
    def blc_summary(self):
        """Return the .blc file if it exists."""
        return self.output.get("blc", None)

    def yearly_summary(self):
        """Return yearly sums of all output variables."""
        return self.csv.resample("YE").sum()
