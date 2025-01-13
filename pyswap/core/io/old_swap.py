import inspect
import re
from pathlib import Path

import pandas as pd
import pandera as pa

from pyswap.components import (
    BottomBoundary,
    Crop,
    Drainage,
    Evaporation,
    FixedIrrigation,
    GeneralSettings,
    HeatFlow,
    Meteorology,
    RichardsSettings,
    SnowAndFrost,
    SoilMoisture,
    SoilProfile,
    SoluteTransport,
    SurfaceFlow,
    tables,
)
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.io.io_ascii import open_ascii
from pyswap.model import Model


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


def parse_ascii_file(file_content) -> tuple[dict, dict]:
    """Parse an ASCII file in SWAP format.

    !!! note "Assumptions"
        - key-value pairs are lines with a single `=` character
        - tables are lines with multiple values separated by whitespace
        - tables are followed by an empty line or a line that is not
          a part of another table.
    """
    lines = file_content.splitlines()
    pairs = {}
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
            table = parse_table(lines, i + 1, key)
            pairs.update(table)
            i += len(list(table.values())[0]) + 1  # Skip the tag data

        elif is_table(line):
            table = parse_table(lines, i + 1, line)
            tables.update(table)
            i += len(list(table.values())[0]) + 1  # Skip the table rows
        i += 1  # Move to the next line

    return pairs, tables


def create_schema_dict():
    """Create a dictionary of all classes from the tables module."""
    schema_dict = {}
    for _, obj in inspect.getmembers(tables):
        if (
            inspect.isclass(obj)
            and issubclass(obj, pa.SchemaModel)
            and obj != pa.SchemaModel
        ):
            schema_fields = tuple(obj.to_schema().columns.keys())
            schema_dict[schema_fields] = obj
    return schema_dict


def create_schema_object(data_dict):
    schema_objects = {}
    schema_dict = create_schema_dict()

    for key, value in data_dict.items():
        if not isinstance(key, tuple):
            continue

        # Use frozenset to ignore order of columns
        columns_set = frozenset(key)
        matching_schema = None

        for schema_columns, schema in schema_dict.items():
            if frozenset(schema_columns) == columns_set:
                matching_schema = schema
                break

        if matching_schema:
            df = pd.DataFrame(value, columns=key)
            try:
                schema_object = matching_schema.validate(df)
                schema_objects[matching_schema.__name__.lower()] = schema_object
            except pa.errors.SchemaError as e:
                print(f"Validation error for {matching_schema.__name__}: {e!s}")
        else:
            print(f"No matching schema found for columns: {key}")

    return schema_objects


def load_swp(path: Path, metadata: PySWAPBaseModel) -> PySWAPBaseModel:
    """Load a SWAP model from a .swp file.

    Parameters:
        path (Path): Path to the .swp file.

    Returns:
        PySWAPBaseModel: The loaded model.
    """
    swp = open_ascii(path)
    text = remove_comments(swp)
    pairs, tables = parse_ascii_file(text)
    schema_objects = create_schema_object(tables)

    # pairs = {k: (int(v) if k.startswith("sw") else v) for k, v in pairs.items()}

    params = pairs | schema_objects

    for k, v in params.items():
        print(k, "=", v)
    # model definition
    model_setup = {
        "generalsettings": GeneralSettings(),
        "meteorology": Meteorology(),
        "crop": Crop(),
        "fixedirrigation": FixedIrrigation(),
        "soilmoisture": SoilMoisture(),
        "surfaceflow": SurfaceFlow(),
        "evaporation": Evaporation(),
        "soilprofile": SoilProfile(),
        "snowandfrost": SnowAndFrost(),
        "richards": RichardsSettings(),
        "lateraldrainage": Drainage(),
        "bottomboundary": BottomBoundary(),
        "heatflow": HeatFlow(),
        "solutetransport": SoluteTransport(),
    }

    for key, value in model_setup.items():
        value.update(params, inplace=True)

    ml = Model(metadata=metadata, **model_setup)

    return ml
