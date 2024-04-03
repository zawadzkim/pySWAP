"""Field serializers"""
from pandas import DataFrame


def serialize_table(table: DataFrame):
    table.columns = [header.upper() for header in table.columns]
    return table.to_string(index=False)


def serialize_csv_table(table: DataFrame):
    table.Station = table.Station.apply(
        lambda x: f"'{x}'" if not str(x).startswith("'") else x)
    return table.to_csv(index=False)
