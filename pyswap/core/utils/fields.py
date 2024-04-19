"""Module for custom field types"""

from typing_extensions import Annotated
from typing import List
from .serializers import serialize_table, serialize_csv_table, serialize_arrays, serialize_object_list
from pandas import DataFrame
from datetime import date as d
from pydantic.functional_serializers import PlainSerializer


Table = Annotated[DataFrame, PlainSerializer(
    lambda x: serialize_table(x), return_type=str, when_used='json')]

# Arrays are used in the .crp file. The problem is that they are not supposed to
# contain headers and the variables (keys) are the same for all options (DFs might
# contain different column names). Need to find a way to ensure the appropriate table is
# passed to the crop file.
Arrays = Annotated[DataFrame, PlainSerializer(
    lambda x: serialize_arrays(x), return_type=str, when_used='json')]

CSVTable = Annotated[DataFrame, PlainSerializer(
    lambda x: serialize_csv_table(x), return_type=str, when_used='json')]

DayMonth = Annotated[d, PlainSerializer(
    lambda x: f"{x.strftime('%d %m')}", return_type=str, when_used='json')]

StringList = Annotated[List[str], PlainSerializer(
    lambda x: ','.join(x), return_type=str, when_used='json')]

FloatList = Annotated[List[float], PlainSerializer(
    lambda x: ' '.join([str(f) for f in x]), return_type=str, when_used='json')]

DateList = Annotated[List[d], PlainSerializer(
    lambda x: '\n' + '\n'.join([d.strftime('%Y-%m-%d') for d in x]), return_type=str, when_used='json')]

Switch = Annotated[bool | int, PlainSerializer(
    lambda x: int(x), return_type=int, when_used='json')]

ObjectList = Annotated[list, PlainSerializer(
    lambda x: serialize_object_list(x), return_type=str, when_used='json'
)]
