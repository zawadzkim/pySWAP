import pandas as pd
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import Table, Arrays

def test_table_serialization():
    class ModelWithTable(PySWAPBaseModel):
        table_: Table

    sample_data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(sample_data)
    model = ModelWithTable(table_=df)

    serialized = model.model_string()
    expected_output = ' A  B\n 1  4\n 2  5\n 3  6\n'

    assert serialized == expected_output, f'Expected: {expected_output}, but got: {serialized}'

def test_arrays_serialization():
    class ModelWithArrays(PySWAPBaseModel):
        arrays: Arrays

    sample_data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(sample_data)
    model = ModelWithArrays(arrays=df)

    serialized = model.model_string()
    expected_output = 'ARRAYS = \n1 4\n2 5\n3 6\n\n'

    assert serialized == expected_output, f'Expected: {expected_output}, but got: {serialized}'