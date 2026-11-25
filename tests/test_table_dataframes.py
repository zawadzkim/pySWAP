"""Table fields accept a plain pandas DataFrame, validated with the schema of
the same name, as well as the result of `<SCHEMA>.create(...)`."""

import pandas as pd
import pandera.errors
import pytest
from pydantic import ValidationError

from pyswap import components
from pyswap.components.tables import INTERTB

INTERTB_DATA = {
    "T": [0.0, 180.0, 366.0],
    "PFREE": [0.9, 0.9, 0.9],
    "PSTEM": [0.05, 0.05, 0.05],
    "SCANOPY": [0.4, 0.4, 0.4],
    "AVPREC": [6.0, 6.0, 6.0],
    "AVEVAP": [1.5, 1.5, 1.5],
}


def test_dataframe_and_create_give_the_same_table():
    from_df = components.Interception(swinter=2, intertb=pd.DataFrame(INTERTB_DATA))
    from_create = components.Interception(
        swinter=2, intertb=INTERTB.create(INTERTB_DATA)
    )
    pd.testing.assert_frame_equal(from_df.intertb, from_create.intertb)
    assert from_df.model_string() == from_create.model_string()


def test_dataframe_columns_are_upper_cased():
    df = pd.DataFrame(INTERTB_DATA).rename(columns=str.lower)
    interception = components.Interception(swinter=2, intertb=df)
    assert list(interception.intertb.columns) == list(INTERTB_DATA)


def test_invalid_dataframe_is_rejected():
    bad = pd.DataFrame(INTERTB_DATA | {"PFREE": [0.9, 1.5, 0.9]})  # PFREE > 1
    with pytest.raises((ValidationError, pandera.errors.SchemaError)):
        components.Interception(swinter=2, intertb=bad)


def test_invalid_dataframe_is_rejected_on_assignment():
    interception = components.Interception(
        swinter=2, intertb=INTERTB.create(INTERTB_DATA)
    )
    with pytest.raises((ValidationError, pandera.errors.SchemaError)):
        interception.intertb = pd.DataFrame(INTERTB_DATA | {"T": [0.0, 180.0, 400.0]})
