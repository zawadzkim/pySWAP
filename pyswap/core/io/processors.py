# ruff: noqa: C901
# mypy: disable-error-code="call-overload, attr-defined"
# error C901 was raised for the parse_ascii_file function. The function indeed
# could use refactoring, but for now we keep it as it is.
# attribute defined was causing issue with the __name__ dunder method, which was
# wrong. Call overload was raised on the create schema function call.

"""Module processing various elements encountered in files.

Processors in this module:
- TableProcessor
"""

from typing import Optional, Literal
from functools import cache
import pandera as pa
import pyswap.components.tables as tables
from pyswap.core.basemodel import BaseTableModel
import logging

import pandas as pd


import inspect

logger = logging.getLogger(__name__)

class TableProcessor:
    def __init__(self):
        self.schemas = self.get_schemas_with_columns()
        logger.debug("TableProcessor initialized.")

    @staticmethod
    def is_dataframe_schema(member) -> bool:
        """Check if a member is a class and not a subclass of pd.Series or BaseTableModel.

        Parameters:
            member (Any): A member to check.
        """
        cond = (
            inspect.isclass(member)
            and not issubclass(member, pd.Series)
            and member is not BaseTableModel
        )
        return cond

    @staticmethod
    def match_schema_by_columns(data_columns: tuple, schema_columns: tuple) -> bool:
        """Check if data columns are a subset of schema columns.

        Parameters:
            data_columns (tuple): A tuple of column names from the data parsed from
                ascii files.
            schema_columns (tuple): A tuple of column names from the schema.
        """
        return frozenset(data_columns).issubset(frozenset(schema_columns["cols"]))

    @staticmethod
    @cache
    def get_schemas_with_columns() -> list[dict]:
        """Create a list of dictionaries with table names, classes and columns names."""
        members = inspect.getmembers(tables, TableProcessor.is_dataframe_schema)
        return [
            {"name": v[0], "class": v[1], "cols": tuple(v[1].to_schema().columns.keys())}
            for v in members
        ]

    @staticmethod
    def create_schema_object(
        schema: BaseTableModel, columns: list, data: list
    ) -> BaseTableModel:
        """Create a schema object from a list of data.

        Parameters:
            schema (BaseTableModel): A schema class to validate the data.
            columns (list): A list of column names.
            data (list): A list of data to validate.
        """
        df = pd.DataFrame(data, columns=columns)
        try:
            schema_object = schema.validate(df)
        except pa.errors.SchemaError as e:
            logger.error(f"Validation error for {schema.__name__}: {e!s}")
            return None
        else:
            logger.debug(f"Successfully validated {schema.__name__}")
            return schema_object

    def process(self, 
                type: Literal["table", "array"], 
                data: dict | list[dict], 
                columns: list[str] | tuple[str], grass = False) -> dict[str, pd.DataFrame] | None:
        """Process the data and return a DataFrame.

        Parameters:
            data (dict | list[dict]): The data to process.
            columns (list[str] | tuple[str]): The columns to include in the DataFrame.

        Returns:
            pd.DataFrame | None: The processed DataFrame or None if processing failed.
        """
        if not data:
            logger.warning("No data provided to process")
            return None

        if type == "table":
            for schema in self.schemas:
                if self.match_schema_by_columns(columns, schema):
                    logger.debug(f"Matched table schema: {schema['name']}")
                    schema_obj = self.create_schema_object(
                        schema["class"], columns, data
                    )
                    if schema_obj is not None:
                        return {schema["name"].lower(): schema_obj}
            
            logger.warning(f"No matching table schema found for columns: {columns}")
            return None
        
        else:
            array_name = columns[0] if isinstance(columns, (list, tuple)) else columns
            for schema in self.schemas:
                    # if the array is a grass crop, remove DVS column from the set.
                    # Otherwise remocve DNR column. This is done to still provide
                    # data validation and sustain the idea of matching the schema
                    # with the parameter by schema name.

                if schema["name"].lower() == array_name.lower():
                    logger.debug(f"Matched array schema: {schema['name']}")
                    
                    # Create a copy of columns to avoid mutating cached schema
                    filtered_cols = tuple(
                        col for col in schema["cols"] 
                        if col.upper() != ("DVS" if grass else "DNR")
                    )
                    
                    schema_obj = self.create_schema_object(
                        schema["class"], filtered_cols, data
                    )
                    if schema_obj is not None:
                        return {schema["name"].lower(): schema_obj}
            
            logger.warning(f"No matching array schema found for: {array_name}")
            return None


def is_dataframe_schema(member) -> bool:
    """Check if a member is a class and not a subclass of pd.Series or BaseTableModel.

    Parameters:
        member (Any): A member to check.
    """
    cond = (
        inspect.isclass(member)
        and not issubclass(member, pd.Series)
        and member is not BaseTableModel
    )
    return cond


def get_schemas_with_columns() -> list[dict]:
    """Create a list of dictionaries with table names, classes and columns names."""
    members = inspect.getmembers(tables, is_dataframe_schema)
    members_with_columns = [
        {"name": v[0], "class": v[1], "cols": tuple(v[1].to_schema().columns.keys())}
        for v in members
    ]
    return members_with_columns


def match_schema_by_columns(data_columns: tuple, schema_columns: tuple) -> bool:
    """Check if data columns are a subset of schema columns.

    Parameters:
        data_columns (tuple): A tuple of column names from the data parsed from
            ascii files.
        schema_columns (tuple): A tuple of column names from the schema.
    """
    return frozenset(data_columns).issubset(frozenset(schema_columns["cols"]))


def create_schema_object(
    schema: BaseTableModel, columns: list, data: list
) -> BaseTableModel:
    """Create a schema object from a list of data.

    Parameters:
        schema (BaseTableModel): A schema class to validate the data.
        columns (list): A list of column names.
        data (list): A list of data to validate.
    """
    df = pd.DataFrame(data, columns=columns)
    try:
        schema_object = schema.validate(df)
    except pa.errors.SchemaError as e:
        msg = f"Validation error for {schema.__name__}: {e!s}"
        print(msg)
        return None
    else:
        return schema_object


def create_table_objects(data_dict: dict) -> dict:
    """Create table objects.

    Parameters:
        data_dict (dict): A dictionary with table names as keys (tuple of column names to match).

    Returns:
        dict: A dictionary with table names as keys and validated schema objects as values.
    """
    schemas = get_schemas_with_columns()
    table_objects = {}

    for key, value in data_dict.items():
        if not isinstance(key, tuple):
            continue

        for schema in schemas:
            if match_schema_by_columns(key, schema):
                table_objects[schema["name"].lower()] = create_schema_object(
                    schema["class"], key, value
                )
                break

    return table_objects


def create_array_objects(data_dict: dict, grass_crp: bool = False) -> dict:
    """Create array objects by matching the name of the array (position 0 in the tuple)

    Parameters:
        data_dict (dict): A dictionary with array names as keys (tuple of column names to match).
        grass_crp (bool): Whether the array is a grass crop. This parameter is used to remove
            the DVS column from the set of columns if the array is a grass crop. Otherwise the
            DNR column is removed. This is because the grass module relies on the day number
            instead of development stage.
    """
    schemas = get_schemas_with_columns()
    array_objects = {}

    for key, value in data_dict.items():
        for schema in schemas:
            data_item_name = key[0].lower() if isinstance(key, tuple) else key.lower()
            if data_item_name == schema["name"].lower():
                # if the array is a grass crop, remove DVS column from the set.
                # Otherwise remocve DNR column. This is done to still provide
                # data validation and sustain the idea of matching the schema
                # with the parameter by schema name.

                if grass_crp:
                    schema["cols"] = tuple(
                        col for col in schema["cols"] if col.upper() != "DVS"
                    )
                else:
                    schema["cols"] = tuple(
                        col for col in schema["cols"] if col.upper() != "DNR"
                    )
                array_objects[schema["name"].lower()] = create_schema_object(
                    schema["class"], schema["cols"], value
                )
                break

    return array_objects