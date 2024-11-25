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

    def model_string(self) -> str:
        """Returns a custom model string representation that matches the
        requirements of .swp file.

        Note:
            If values are simple types, they are formatted as 'ATTR = VALUE'.
            If the valies are tables (in pySWAP pd.DataFrame are used), they
            are formatted simply as 'TABLE_VALUE'. Additionally, a custom
            serializer (pyswap.core.utils.serializers.quote_string)
            is used to quote strings
        Returns:
            str: Custom model string representation.
        """
        string = ""

        def formatter(attr, value, string):
            if attr.startswith("table_") or attr.startswith("list_"):
                return string + value
            else:
                return string + f"{attr.upper()} = {value}\n"

        for attr, value in self.model_dump(mode="json", exclude_none=True).items():
            if isinstance(value, dict):
                for k, v in value.items():
                    string = formatter(k, v, string)
            else:
                string = formatter(attr, value, string)

        return string

    def _concat_sections(self) -> str:
        """Concatenate a string from individual sections.

        This method is meant to be used on models that collect other
        models, like DraFile, or Model.
        """

        string = ""
        for k, v in dict(self).items():
            if v is None or isinstance(v, str):
                continue
            string += v.model_string()
        return string


class BaseTableModel(pa.DataFrameModel):
    """Base model for pandas DataFrames.
    
    Methods:
        create: Create a validated DataFrame from a dictionary.
    """

    class Config:
        coerce = True

    @classmethod
    def create(cls, data: dict) -> DataFrame:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()
        validated_df = cls.validate(df)
        return validated_df
