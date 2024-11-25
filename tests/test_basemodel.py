import pytest
from pydantic import BaseModel
from pyswap.core import PySWAPBaseModel

# def test_pyswap_base_model_initialization(simple_model):
#     assert isinstance(simple_model, PySWAPBaseModel)
#     assert isinstance(simple_model, BaseModel)


def test_model_string_with_none_values(simple_model):
    model = simple_model(attr1="test", attr2=12, table_data="1 2 3")
    expected_output = "ATTR1 = test\nATTR2 = 12\n1 2 3"
    assert model.model_string() == expected_output, f"Expected: \n {expected_output} \n but got \n {model.model_string()}"

# def test_concat_sections(complex_model, expected_complex_output):
#     assert complex_model._concat_sections() == expected_complex_output

# def test_model_config(expected_config):
#     assert PySWAPBaseModel.model_config == expected_config

# def test_model_string_with_dict(dict_model, expected_dict_output):
#     assert dict_model.model_string() == expected_dict_output

# def test_formatter(formatter_test_case):
#     attr, value, expected = formatter_test_case
#     model = TestModel(**{attr: value})
#     assert model.model_string() == expected

# def test_model_string_empty(empty_model):
#     assert empty_model.model_string() == ""