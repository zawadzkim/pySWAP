# mypy: disable-error-code="no-any-return"


"""Capturing model results.

After a model is run, the results are stored in a `Result` object. The object
stores the log file, output file, and warnings. Output is a dictionary with
the keys being the file extensions and the values being the file contents. There
are also computed properties making the most common output formats easily
accessible.

Classes:
    Result: Result of a model run.
"""

import re

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field, computed_field

__all__ = ["Result"]


class Result(BaseModel):
    """Result of a model run.

    Attributes:
        log (str): The log file of the model run.
        output (DataFrame): The output file of the model run.
        warning (List[str]): The warnings of the model run.

    Properties:
        ascii (dict): The output in ASCII format.
        csv (DataFrame): The output in CSV format.
        csv_tz (DataFrame): The output in CSV format with depth.
        iteration_stats (str): Return the part the iteration statistics from
            the log.
        blc_summary (str): The .blc file if it exists.
        yearly_summary (DataFrame): Yearly sums of all output variables. Will
            return an error if csv was not included in the output file formats.
    """

    log: str | None = Field(default=None, repr=False)
    output: dict | None = Field(default_factory=dict, repr=False)
    warning: list[str] | None = Field(default=None, repr=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    @computed_field(return_type=dict, repr=False)
    def ascii(self) -> dict:
        """Return all outputs in ASCII format."""
        return {k: v for k, v in self.output.items() if not k.endswith("csv")}

    @computed_field(return_type=DataFrame, repr=False)
    def csv(self) -> DataFrame:
        """Return the output in CSV format."""
        return self.output.get("csv", None)

    @computed_field(return_type=DataFrame, repr=False)
    def csv_tz(self) -> DataFrame:
        """Return the output in CSV format with depth."""
        return self.output.get("csv_tz", None)

    @computed_field(return_type=str, repr=False)
    def iteration_stats(self) -> str:
        """Print the part the iteration statistics from the log."""
        match = re.search(r".*(Iteration statistics\s*.*)$", self.log, re.DOTALL)
        if match:
            return match.group(1)
        return ""

    @computed_field(return_type=str, repr=False)
    def blc_summary(self) -> str:
        """Print the .blc file if it exists."""
        print(self.output.get("blc", None))
        return

    @computed_field(return_type=DataFrame, repr=False)
    def yearly_summary(self) -> DataFrame:
        """Return yearly sums of all output variables."""
        if not isinstance(self.csv, DataFrame):
            msg = "CSV file not included in output file formats."
            raise TypeError(msg)
        return self.csv.resample("YE").sum()
