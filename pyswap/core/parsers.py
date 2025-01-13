"""Functions to parse SWAP formatted ascii files into pySWAP objects.

pySWAP has the ability to interact directly with the classic SWAP input files.
Parsers defined in this module are used for the custom field validators defined
in the `pyswap.core.fields` module. These functions convert (or deserialize) the
SWAP formatted ascii files into pySWAP objects.

Parsers in this module:
    parse_string_list: Convert a SWAP string list to a list of strings.
    parse_quoted_string: Make sure to remove unnecessary quotes from source.
    parse_day_month: Convert a string to a date object with just the day and
        month.
"""

from datetime import date


def parse_string_list(value: str):
    """Convert a SWAP string list to a list of strings."""
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return value.strip("'").split(",")


def parse_quoted_string(value: str):
    """Make sure to remove unnecessary quotes from source."""
    if isinstance(value, str):
        return value.strip("'")
    raise ValueError("Invalid type. Expected string")


def parse_day_month(value: str | date) -> date:
    """Convert a string to a date object with just the day and month."""
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            day, month = map(int, value.split())
            return date(date.today().year, month, day)
        except (ValueError, TypeError):
            raise ValueError("Invalid day-month format. Expected 'DD MM'")
    raise ValueError("Invalid type. Expected date or string 'DD MM'")
