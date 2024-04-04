"""Field serializers"""
from pandas import DataFrame
import re


def serialize_table(table: DataFrame):
    table.columns = [header.upper() for header in table.columns]
    return f'{table.to_string(index=False)}\n'


def serialize_csv_table(table: DataFrame):
    table.Station = table.Station.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x)
    return table.to_csv(index=False)


def quote_string(string: str) -> str:

    if re.search("[a-zA-Z]", str(string)):
        return f'"{string}"'
    else:
        return string
