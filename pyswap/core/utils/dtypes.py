from datetime import date as d
from dataclasses import dataclass
from typing import List
from pandas import DataFrame


@dataclass
class DateList:
    datetime_list: List[d]

    def __repr__(self):
        return '\n' + '\n'.join([date.strftime('%Y-%m-%d') for date in self.datetime_list])


@dataclass
class FloatList:
    float_list: List[float]

    def __repr__(self):
        return ' '.join([f"{f}" for f in self.float_list])


@dataclass
class StringList:
    string_list: List[str]

    def __repr__(self):
        return f"'{','.join([s for s in self.string_list])}'"


@dataclass
class DayMonth:
    date: d

    def __repr__(self):
        return self.datetime.strftime('%d %m')


@dataclass
class Table:
    table: dict[list] | DataFrame

    def __repr__(self):
        if isinstance(self.table, dict):
            uppercase_table = {key.upper(): value for key,
                               value in self.table.items()}
            return DataFrame(uppercase_table).to_string(index=False)
        elif isinstance(self.table, DataFrame):
            uppercase_headers = [header.upper()
                                 for header in self.table.columns]
            self.table.columns = uppercase_headers
            return self.table.to_string()


@dataclass
class Section:
    excluded_fields = ['meteo_data']

    def to_string(self):
        return '\n'.join([f"{str(value)}" if isinstance(value, (Subsection, Table)) else f"{key.upper()} = {value}"
                          for key, value in self.__dict__.items()
                          if value is not None and key not in self.excluded_fields])


@dataclass
class Subsection:
    def __str__(self):
        return '\n'.join([f"{key.upper()} = {int(value) if isinstance(value, bool) else value}"
                          if not isinstance(value, Table) else f"{value}"
                          for key, value in self.__dict__.items()
                          if value is not None])
