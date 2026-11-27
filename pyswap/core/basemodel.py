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
        extra="forbid",
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

        fields = type(self).model_fields
        names = {name: name for name in fields}
        names |= {f.alias: name for name, f in fields.items() if f.alias}
        new = {names[key]: value for key, value in new.items() if key in names}
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

    @field_validator("*", mode="after")
    @classmethod
    def validate_table(cls, value: Any, info: Any) -> Any:
        """Validate a DataFrame against the table schema of the same name.

        A table field (e.g. `gctb`) can be given a plain pandas DataFrame
        instead of the result of `GCTB.create(...)`. Column names are
        upper-cased and the DataFrame is validated (and coerced) with the
        pandera schema named after the field, exactly as `create` does, so
        both ways give the same table. Fields without a schema of that name
        are left as they are.
        """
        if not isinstance(value, pd.DataFrame) or info.field_name is None:
            return value
        schema = _table_schemas().get(info.field_name.upper())
        if schema is None:
            return value
        df = value.copy()
        df.columns = [str(c).upper() for c in df.columns]
        return schema.validate(df)


def _table_schemas() -> dict[str, type[BaseTableModel]]:
    """Table schemas by name, e.g. {"GCTB": GCTB} (imported lazily: the
    tables module itself imports this module)."""
    global _TABLE_SCHEMAS
    if _TABLE_SCHEMAS is None:
        from pyswap.components import tables

        _TABLE_SCHEMAS = {
            name: obj
            for name, obj in vars(tables).items()
            if isinstance(obj, type)
            and issubclass(obj, BaseTableModel)
            and obj is not BaseTableModel
        }
    return _TABLE_SCHEMAS


_TABLE_SCHEMAS: dict[str, type[BaseTableModel]] | None = None


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
