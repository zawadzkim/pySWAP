# mypy: disable-error-code="attr-defined"
# attr-defined is disabled because it was easier to implement part of the
# functionality of one mixin in the base class. Could be considered to be
# fixed later.
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

from typing import Any

import pandas as pd
import pandera.pandas as pa
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, field_validator

from pyswap.core.defaults import ADDITIONAL_SWITCHES


class PySWAPBaseModel(BaseModel):
    """Base class for pySWAP models.

    Methods:
        __setattr__: Overriden method to silently ignore assignment of frozen
            fields.
        update: Update the model with new values from a dictionary.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="ignore",
        populate_by_name=True,
    )

    def __setattr__(self, name, value):
        """Silently ignore assignment of frozen fields.

        This method is overridden to silently ignore assignment of frozen fields
        to avoid errors when an old swp files is read.
        """
        _class = type(self)

        if name in _class.model_fields and _class.model_fields[name].frozen:
            return
        super().__setattr__(name, value)

    def update(self, new: dict, inplace: bool = False, no_validate: bool = False):
        """Update the model with new values.

        Given dictionary of values is first filtered to include only the fields
        that exist in the model. The model is then updated with the new values.
        The updated model is returned (either new or updated self).

        Parameters:
            new (dict): Dictionary with new values.
            inplace (bool): If True, update the model in place.
        """

        updated_model = self.model_validate(dict(self) | new)

        if not inplace:
            # added this for the case when the user loads a model from the
            # classic ASCII files. Then the .update() method is used, but not
            # all the attributes will be available immediatelly. Full validation
            # will still be performed upon model run.
            if no_validate:
                updated_model._validation = False
            else:
                updated_model._validation = True
            updated_model.validate_with_yaml() if hasattr(
                updated_model, "validate_with_yaml"
            ) else None
            return updated_model.model_copy(deep=True)

        else:
            for field, value in updated_model:
                setattr(self, field, value)
            if no_validate:
                updated_model._validation = False
            else:
                updated_model._validation = True
            self.validate_with_yaml() if hasattr(
                updated_model, "validate_with_yaml"
            ) else None

            return self

    @field_validator("*", mode="before")
    @classmethod
    def convert_switches(cls, value: Any, info: Any) -> Any:
        """Convert switch values to integers.

        This method was necessary to ensure that loading models from ASCII files
        would work. It could be improved to include literals that do not start
        with "sw" as well.

        !!! note:
            This should be eventually replaced by a custom Switch field type handling
            serialization and deserialization.
        """
        if (
            (info.field_name.startswith("sw") or info.field_name in ADDITIONAL_SWITCHES)
            and info.field_name != "swap_ver"
            and value
        ):
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
        df = pd.DataFrame(data=data)
        if columns:
            df.columns = columns
        else:
            df.columns = df.columns.str.upper()
        validated_df = cls.validate(df)
        return validated_df

    @classmethod
    def update(cls, table, new: dict):
        # Update the table with new values
        table_upd = table.to_dict("list")
        table_upd.update(new)
        return cls.create(table_upd)
