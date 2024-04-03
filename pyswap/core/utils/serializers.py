"""Field serializers"""
from pandas import DataFrame


def serialize_table(table: DataFrame):
    table.columns = [header.upper() for header in table.columns]
    return table.to_string(index=False)
