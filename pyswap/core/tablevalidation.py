"""Pandera schemas for validating tables in pySWAP.

The schemas are used to validate pandas DataFrames used in the pySWAP models.
They also help to enforce the appropriate data types required
by the SWAP model.

Classes:
    BaseModel: Base class for all pySWAP schemas.
"""

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame


class BaseTableModel(pa.DataFrameModel):
    """Base model with create method for preprocessing and validation."""

    class Config:
        coerce = True

    @classmethod
    def create(cls, data: dict) -> DataFrame:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()
        validated_df = cls.validate(df)
        return validated_df
