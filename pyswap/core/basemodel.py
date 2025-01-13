"""Base models inherited by all pySWAP models.

A lot of functionality can be abstracted away in the base models. This way, the
code is more DRY and easier to maintain. The base models are used to enforce
the correct data types and structure of the input data. They also provide
methods to convert the data to the format required by the SWAP model.

Classes defined here are based on Pydantic BaseModel and Pandera DataFrameModel.
Both are meant to ensure the correct data types and structure of the input data,
as successful validation means smooth execution of the SWAP model. Particularily
important when run as a submitted job on an HPC.

Classes:
    BaseModel: Base class for pySWAP models. Inherits from Pydantic BaseModel.
    BaseTableModel: Base class for pySWAP models that validate pandas
        DataFrames. Inherits from Pandera DataFrameModel.
"""

from __future__ import annotations

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, PrivateAttr
from pydantic import field_validator
from typing import Any


class PySWAPBaseModel(BaseModel):
    """Base class for pySWAP models.

        Methods:
            __setattr__: Overriden method to silently ignore assignment of frozen
                fields.
            update: Update the model with new values from a dictionary.
    d"""

    _validation = PrivateAttr(default=False)
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    def __setattr__(self, name, value):
        """Silently ignore assignment of frozen fields.

        This method is overridden to silently ignore assignment of frozen fields
        to avoid errors when an old swp files is read.

        Parameters:
            name: The name of the attribute.
            value: The value of the attribute.
        """

        if name in self.model_fields and self.model_fields[name].frozen:
            return
        super().__setattr__(name, value)

    def update(self, new: dict, inplace: bool = False):
        """Update the model with new values.

        Given dictionary of values is first filtered to include only the fields
        that exist in the model. The model is then updated with the new values.
        The updated model is returned (either new or updated self).

        Parameters:
            new (dict): Dictionary with new values.
            inplace (bool): If True, update the model in place.
        """

        filtered = {k: v for k, v in new.items() if k in self.model_fields}

        updated_model = self.model_validate(self.model_dump() | filtered)

        if not inplace:
            updated_model._validation = True
            updated_model.validate_with_yaml() if hasattr(
                updated_model, "validate_with_yaml"
            ) else None
            return updated_model

        else:
            for field, value in updated_model:
                setattr(self, field, value)

            self._validation = True
            self.validate_with_yaml() if hasattr(
                updated_model, "validate_with_yaml"
            ) else None

            return self

    @field_validator("*", mode="before")
    @classmethod
    def convert_switches(cls, value: Any, info: Any) -> Any:
        """Convert switch values to integers.

        This method was necessary to ensure that loading models from ASCII files
        would work.
        """
        if info.field_name.startswith("sw") and info.field_name != "swap_ver" and value:
            try:
                return int(value)
            except ValueError:
                return value
        return value


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
