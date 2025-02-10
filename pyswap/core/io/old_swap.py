import inspect
import re

import pandas as pd
import pandera as pa

import pyswap.components.tables as tables
from pyswap.core.basemodel import BaseTableModel

def remove_comments(text: str) -> str:
    """Remove comments from a SWAP input file.

    In a SWAP input files some lines are comments. Full line comments
    start with a * character. Partial comments start with a ! character and
    sometimes follow the actual data.

    !!! note
        Empty lines are not removed at this stage. They are important for
        parsing the tables.

    Parameters:
        text (str): The text to remove comments from.

    Returns:
        str: Stripped text with comments removed.
    """
    # Remove lines starting with *
    text = re.sub(r"^\*.*$", "", text, flags=re.MULTILINE)
    # Remove everything after ! on each line
    text = re.sub(r"!.*", "", text)

    return text.strip()


def parse_ascii_file(file_content) -> dict[str, dict]:
    """Parse an ASCII file in SWAP format.

    !!! note "Assumptions"
        - key-value pairs are lines with a single `=` character
        - tables are lines with multiple values separated by whitespace
        - tables are followed by an empty line or a line that is not
          a part of another table.

    Parameters:
        file_content (str): The content of the ASCII file.

    Returns:
        dict: A dictionary with key-value pairs, arrays and tables
            (in the exact order).
    """
    lines = file_content.splitlines()
    pairs = {}
    arrays = {}
    tables = {}

    def is_key_value(line):
        return (
            "=" in line
            and not line.strip().startswith("=")
            and not line.strip().endswith("=")
        )

    def format_key_value(line):
        key, value = line.split("=", 1)
        return {key.strip().lower(): value.strip()}

    def is_table(line):
        """Check if the line is a part of a table.

        A table is essentially everything else than a key-value pair or
        an empty tag except empty lines.
        """
        return line.strip() and "=" not in line and not line.strip().endswith("=")

    def is_empty_tag(line):
        """Check if the line is an empty tag.

        An empty tag is a line where there is only the tag folloed by an = sign (e.g., DZNEW =)
        and the data for that tag is in the next line(s). This is most common for tables,
        which in pySWAP are called ARRAYS - tables with no header, but values groupped in
        columns separated by spaces."""

        return line.strip().endswith("=")

    def parse_table(lines, start_index, key):
        """Parse a table from the list of lines.

        This function is triggered if a line is detected as an empty tag or a table. It will
        assume all lines after the empty tag or the table header are part of the table until
        an empty line or a line that is not part of the table is found. Those lines are then
        stored in a list, later used to skip the table rows before parsing the next item.
        """
        data = []
        for line in lines[start_index:]:
            if line.strip() and not is_key_value(line) and not is_empty_tag(line):
                data.append(line.strip().split())
            else:
                break
        return {tuple(key.strip().split()): data}

    i = 0
    # loop over the list of lines, stripping each
    while i < len(lines):
        line = lines[i].strip()

        if is_key_value(line):
            pairs.update(format_key_value(line))

        elif is_empty_tag(line):
            key = line[:-1].strip()
            array = parse_table(lines, i + 1, key)
            arrays.update(array)
            i += len(list(array.values())[0]) + 1  # Skip the tag data

        elif is_table(line):
            table = parse_table(lines, i + 1, line)
            tables.update(table)
            i += len(list(table.values())[0]) + 1  # Skip the table rows
        i += 1  # Move to the next line

    return pairs, arrays, tables

def member_conditions(member) -> bool:
    """Check if a member is a class and not a subclass of pd.Series or BaseTableModel."""
    cond = (inspect.isclass(member) and 
            not issubclass(member, pd.Series) and 
            member is not BaseTableModel)
    return cond

def tables_columns_dict() -> list[dict]:
    """Create a list of dictionaries with table names, classes and columns names."""
    members = inspect.getmembers(tables, member_conditions)
    members_with_columns = [{"name": v[0], "class": v[1], "cols": tuple(v[1].to_schema().columns.keys())} for v in members]
    return members_with_columns

def match_schema_by_columns(data_columns: tuple, schema_columns: tuple) -> bool:
    """Check if data columns are a subset of schema columns."""
    return frozenset(data_columns).issubset(frozenset(schema_columns["cols"]))

def create_schema(schema: BaseTableModel, columns: list, data: list) -> BaseTableModel:
    """Create a schema object from a list of data."""
    df = pd.DataFrame(data, columns=columns)
    try:
        schema_object = schema.validate(df)
        return schema_object
    except pa.errors.SchemaError as e:
        print(f"Validation error for {schema.__name__}: {e!s}")

def create_table_objects(data_dict: dict) -> dict:
    """Create table objects by matching the columns with the schema objects.
    
    Parameters:
        data_dict (dict): A dictionary with table names as keys (tuple of column names to match).

    Returns:
        dict: A dictionary with table names as keys and validated schema objects as values.
    """
    schemas = tables_columns_dict()
    table_objects = {}

    for key, value in data_dict.items():
        if not isinstance(key, tuple):
            continue

        for schema in schemas:
            if match_schema_by_columns(key, schema):
                table_objects[schema["name"].lower()] = create_schema(schema["class"], key, value)
                break

    return table_objects

def create_array_objects(data_dict: dict, grass_crp: bool = False) -> dict:
    """Create array objects by matching the name of the array (position 0 in the tuple)"""
    schemas = tables_columns_dict()
    array_objects = {}

    for key, value in data_dict.items():
        if not isinstance(key, tuple):
            continue

        for schema in schemas:
            if key[0].lower() == schema["name"].lower():
                # if the array is a grass crop, remove DVS column from the set.
                # Otherwise remocve DNR column. This is done to still provide
                # data validation and sustain the idea of matching the schema
                # with the parameter by schema name.
                if grass_crp:
                    schema["cols"] = tuple(col for col in schema["cols"] if col.upper() != "DVS")
                else:
                    schema["cols"] = tuple(col for col in schema["cols"] if col.upper() != "DNR")

                array_objects[schema["name"].lower()] = create_schema(schema["class"], schema["cols"], value)
                break

    return array_objects

