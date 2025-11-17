"""Module processing ASCII files in SWAP format.

Steps to process SWAP format ASCII files:
1. Identify and remove comments.
2. Parse the remaining content into key-value pairs, tables and arrays.
"""

import logging
import re

from pyswap.core.io.processors import TableProcessor

logger = logging.getLogger(__name__)


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

    text = re.sub(r"(^\*.*$|!.*)", "", text, flags=re.MULTILINE)

    return text.strip()


def parse_ascii_file(file_content, grass=False) -> dict[str, dict]:
    """Parse an ASCII file in SWAP format.

    !!! note "Assumptions"
        - key-value pairs are lines with a single `=` character
        - tables are lines in which columns are split by spaces
        - empty tags are lines that end with an `=` character, followed by
            table-like data in the following lines.
        - tables are followed by an empty line or a line that is not
          a part of another table.

    Parameters:
        file_content (str): The content of the ASCII file.

    Returns:
        dict: A dictionary with key-value pairs, arrays and tables
            (in the exact order).
    """
    cleaned_file = remove_comments(file_content)
    lines = cleaned_file.splitlines()
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

    def parse_table(lines, start_index, key, param_type):
        """Parse a table from the list of lines.

        This function is triggered if a line is detected as an empty tag or a table. It will
        assume all lines after the empty tag or the table header are part of the table until
        an empty line or a line that is not part of the table is found. Those lines are then
        stored in a list, later used to skip the table rows before parsing the next item.
        """
        data = []
        tp = TableProcessor()
        for line in lines[start_index:]:
            if line.strip() and not is_key_value(line) and not is_empty_tag(line):
                data.append(line.strip().split())
            else:
                break
        processed = tp.process(
            data_type=param_type,
            data=data,
            columns=tuple(key.strip().split()),
            grass=grass,
        )
        logger.debug(f"Processed {len(data)} rows for {key.strip()}")
        return processed, len(data)

    i = 0
    # loop over the list of lines, stripping each

    while i < len(lines):
        line = lines[i].strip()

        if is_key_value(line):
            pairs.update(format_key_value(line))

        elif is_empty_tag(line):
            key = line[:-1].strip()
            array = parse_table(
                lines=lines, start_index=i + 1, key=key, param_type="array"
            )
            arrays.update(array[0])
            i += array[1] + 1  # Skip the tag data

        elif is_table(line):
            # The table header is the line itself (de facto dictionary key)
            table = parse_table(
                lines=lines, start_index=i + 1, key=line, param_type="table"
            )
            tables.update(table[0])
            i += table[1] + 1  # Skip the table rows
        i += 1  # Move to the next line

    return pairs | arrays | tables
