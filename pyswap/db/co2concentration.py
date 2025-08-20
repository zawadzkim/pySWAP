from pandas import DataFrame, to_datetime
from pydantic import BaseModel as _BaseModel

from pyswap.core.io.io_csv import load_csv
from pyswap.libs import co2concentration
from pyswap.utils.mixins import FileMixin as _FileMixin


class CO2concentration(_BaseModel, _FileMixin):
    path: str = co2concentration
    _extension: str = "co2"

    def get_filtered_co2file(self, period) -> DataFrame:
        """Get CO2 concentration data for a given period.

        Parameters
        ----------
        period : list
            List of two strings representing the start and end date (e.g. ["2000-01-01", "2020-12-31"]).
        """
        data = load_csv(
            self.path,
            delimiter=" ",
            skiprows=12,
            index_col=0,
        )

        # Convert period to datetime
        period = to_datetime(period)

        # Filter data
        data = data[(data.index >= period[0].year) & (data.index <= period[1].year)]

        return data

    def write_co2(self, directory, period) -> None:
        """Write CO2 concentration data to a file."""
        # Get data for the given period
        data = self.get_filtered_co2file(period)

        # Create datastring
        dstring = data.to_csv(
            index=True,
            float_format="%.2f",
            sep=" ",
            lineterminator="\n",
        )

        # Write to file
        self.save_file(string=dstring, fname="Atmospheric", path=directory)
