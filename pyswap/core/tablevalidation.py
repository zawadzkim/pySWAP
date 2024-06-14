"""Pandera schemas for validating tables in pySWAP.

The schemas are used to validate pandas DataFrames used in the pySWAP models. They also
help to enforce the appropriate data types required by the SWAP model.

!!! warning
    This is an experimental feature and is currently only implemented in the 
    irrigation subpackage. If no bugs are found, it will be implemented in
    the other subpackages.

Attributes:
    irrigation_schema (DataFrameSchema): Validate irrigation data.
"""

import pandera as pa
import pandas as pd
from pandera.typing import DataFrame

irrigation_schema = pa.DataFrameSchema({
    'IRDATE': pa.Column(pa.DateTime),
    'IRDEPTH': pa.Column(float),
    'IRCONC': pa.Column(float, required=False),
    'IRTYPE': pa.Column(int, required=False),
},
    coerce=True
)
"""Validate irrigation data."""


class BaseModel(pa.DataFrameModel):
    """Base model with create method for preprocessing and validation."""

    class Config:
        coerce = True

    @classmethod
    def create(cls, data: dict) -> DataFrame:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()
        validated_df = cls.validate(df)
        return validated_df

