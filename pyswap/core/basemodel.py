"""
# Base models

A lot of functionality can be abstracted away in the base models. This way, the
code is more DRY and easier to maintain. The base models are used to enforce
the correct data types and structure of the input data. They also provide
methods to convert the data to the format required by the SWAP model.

This module defines the base model for regular classes and classes that
validate pandas DataFrames.

Classes:
    BaseModel: Base class for pySWAP models. Inherit on Pydantic BaseModel.
    BaseTableModel: Base class for pySWAP models that validate pandas
        DataFrames. Inherit on Pandera DataFrameModel.
"""



from __future__ import annotations

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator



class PySWAPBaseModel(BaseModel):
    """Base class for pySWAP models.

    Attributes:
        model_config (ConfigDict): Overriding Pydantic model configuration.

    Methods:
        model_string: Returns a custom model string representation that
            matches the requirements of .swp file.
        _concat_sections: Concatenate a string from individual sections.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    name: str | None = Field(default="", exclude=True)

    @model_validator(mode="after")
    def set_name(cls, values):
        if not values.name:
            values.name = cls.__name__.lower()
        return values


class BaseTableModel(pa.DataFrameModel):
    """Base model for pandas DataFrames.
    
    Methods:
        create: Create a validated DataFrame from a dictionary.
    """

    class Config:
        coerce = True

    @classmethod
    def create(cls, data: dict, columns: list | None = None) -> DataFrame:
        df = pd.DataFrame(data)
        if columns:
            df.columns = columns
        else:
            df.columns = df.columns.str.upper()
        validated_df = cls.validate(df)
        return validated_df
