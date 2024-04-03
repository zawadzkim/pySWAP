"""Module for custom field types"""

from typing_extensions import Annotated
from typing import List, Literal
from .serializers import serialize_table
from pandas import DataFrame
from datetime import datetime as d
from pydantic.functional_serializers import PlainSerializer


Table = Annotated[DataFrame, PlainSerializer(
    lambda x: serialize_table(x), return_type=str, when_used='json')]

DayMonth = Annotated[d, PlainSerializer(
    lambda x: x.strftime('%d %m'), return_type=str, when_used='json')]

StringList = Annotated[List[str], PlainSerializer(
    lambda x: ','.join(x), return_type=str, when_used='json')]

FloatList = Annotated[List[float], PlainSerializer(
    lambda x: ' '.join([str(f) for f in x]), return_type=str, when_used='json')]

DateList = Annotated[List[d], PlainSerializer(
    lambda x: '\n' + '\n'.join([d.strftime('%Y-%m-%d') for d in x]), return_type=str, when_used='json')]

Switch = Annotated[bool | int, PlainSerializer(
    lambda x: int(x), return_type=int, when_used='json')]
