import pytest

from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.utils.mixins import SerializableMixin
from pyswap.core.fields import Table, Table, Arrays, DayMonth, StringList, FloatList, IntList, DateList, ObjectList, String, Subsection, Decimal2f, Decimal3f, Decimal4f


@pytest.fixture(scope="module")
def sample_file(tmp_path_factory):
    file_content = """
**********************************************************************************

*** GENERAL SECTION ***

**********************************************************************************
* Part 1: Environment

  PROJECT   = 'swap-test'    ! Project description [A80]
  PATHWORK  = '.\\'           ! Path to work folder [A80]
  PATHATM   = '.\\'   ! Path to folder with weather files [A80]
  PATHCROP  = '.\\'  ! Path to folder with crop files [A80]
  PATHDRAIN = '.\\'           ! Path to folder with drainage files [A80]

* Switch, display progression of simulation run to screen:
  SWSCRE    = 0              ! 0 = no display to screen
                             ! 1 = display water balance components
                             ! 2 = display daynumber
"""
    tmp_dir = tmp_path_factory.mktemp("data")
    file_path = tmp_dir / "test_sample_input.txt"
    with open(file_path, "w") as f:
        f.write(file_content)
    return file_path


# class ComplexModel(PySWAPBaseModel):
#     simple_model: SimpleModel
#     extra_attr: float


@pytest.fixture()
def simple_serializable_model():
    class SimpleModel(PySWAPBaseModel, SerializableMixin):
        table: Table
        arrays: Arrays
        daymonth: DayMonth
        stringlist: StringList
        floatlist: FloatList
        intlist: IntList
        datelist: DateList
        string: String
        decimal2f: Decimal2f
        decimal3f: Decimal3f
        decimal4f: Decimal4f

    return SimpleModel


# def test_model_string_simple():
#     model = SimpleModel(attr1="test", attr2=42, table_data="1 2 3", list_items="a b c")
#     expected_output = "ATTR1 = test\nATTR2 = 42\n1 2 3a b c"
#     assert model.model_string() == expected_output

# def test_model_string_with_none_values():
#     model = SimpleModel(attr1="test", attr2=None, table_data="1 2 3", list_items=None)
#     expected_output = "ATTR1 = test\n1 2 3"
#     assert model.model_string() == expected_output

# def test_concat_sections():
#     simple_model = SimpleModel(attr1="test", attr2=42, table_data="1 2 3", list_items="a b c")
#     complex_model = ComplexModel(simple_model=simple_model, extra_attr=3.14)
#     expected_output = "ATTR1 = test\nATTR2 = 42\n1 2 3a b cEXTRA_ATTR = 3.14\n"
#     assert complex_model._concat_sections() == expected_output


# def test_model_string_with_dict():
#     class DictModel(PySWAPBaseModel):
#         dict_attr: dict

#     model = DictModel(dict_attr={"key1": "value1", "key2": 42})
#     expected_output = "KEY1 = value1\nKEY2 = 42\n"
#     assert model.model_string() == expected_output

# @pytest.mark.parametrize("attr,value,expected", [
#     ("normal_attr", "test", "NORMAL_ATTR = test\n"),
#     ("table_data", "1 2 3", "1 2 3"),
#     ("list_items", "a b c", "a b c"),
# ])
# def test_formatter(attr, value, expected):
#     class TestModel(PySWAPBaseModel):
#         normal_attr: str
#         table_data: str
#         list_items: str

#     model = TestModel(**{attr: value})
#     assert model.model_string() == expected

# def test_model_string_empty():
#     class EmptyModel(PySWAPBaseModel):
#         pass

#     model = EmptyModel()
#     assert model.model_string() == ""
