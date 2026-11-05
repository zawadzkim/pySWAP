from pyswap.components.tables import RDTB
from pyswap.core.io.processors import TableProcessor


def test_create_schema_object_returns_none_for_invalid_data():
    # pandera < 0.31 raises SchemaError for a failed coercion, newer versions
    # raise SchemaErrors; both must be handled.
    result = TableProcessor.create_schema_object(
        RDTB, columns=["DVS", "RD"], data=[[0.0, "deep"], [2.0, 50.0]]
    )
    assert result is None


def test_create_schema_object_returns_none_for_out_of_range_data():
    result = TableProcessor.create_schema_object(
        RDTB, columns=["DVS", "RD"], data=[[0.0, 10.0], [2.0, 5000.0]]
    )
    assert result is None
