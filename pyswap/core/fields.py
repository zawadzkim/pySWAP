"""Custom field types used for serilization in the model_dump(mode='json').

Other parameters:
    Table (DataFrame): A DataFrame object serialized as a string with just the headers and the data.
    Arrays (DataFrame): A DataFrame object serialized as a string with just the columns of data (no headers),
        but with the variable name in front (e.g., FLUXTB = 0.0 0.0/n 1.0 1.0 )
    CSVTable (DataFrame): A DataFrame object serialized as a string with the headers and data in CSV format, 
        specifically tailored for the .met file format.
    DayMonth (d): A date object serialized as a string with just the day and month (e.g., '01 01').
    StringList (List[str]): A list of strings serialized as a string with the elements separated by commas, enclosed
        in quotation marks (e.g., 'string1, string2, string3').
    FloatList (List[float]): A list of floats serialized as a string with the elements separated by spaces.
    DateList (List[d]): A list of date objects serialized as a string with the elements separated by newlines.
    Switch (bool | int): A boolean or integer serialized as an integer (0 or 1).
    ObjectList (list): A list of objects serialized as a string with the elements separated by newlines.   
    """

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

IntList = Annotated[List[int], PlainSerializer(
    lambda x: ' '.join([str(f) for f in x]), return_type=str, when_used='json')]

DateList = Annotated[List[d], PlainSerializer(
    lambda x: '\n' + '\n'.join([d.strftime('%Y-%m-%d') for d in x]), return_type=str, when_used='json')]

Switch = Annotated[bool | int, PlainSerializer(
    lambda x: int(x), return_type=int, when_used='json')]

ObjectList = Annotated[list, PlainSerializer(
    lambda x: serialize_object_list(x), return_type=str, when_used='json'
)]
