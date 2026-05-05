import pandas as pd

import pyswap.components.crop as crp


def test_model_serialization(simple_serializable_model):
    tabular_data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    model = simple_serializable_model(
        table=tabular_data,
        arrays=tabular_data,
        daymonth="12 01",
        stringlist=["a", "b", "c"],
        floatlist=[1.0, 2.0, 3.0],
        intlist=[1, 2, 3],
        datelist=[pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02")],
        string="string",
        decimal2f=1.0,
        decimal3f=1.0,
        decimal4f=1.0,
    )

    expected_output = " col1  col2\n    1     4\n    2     5\n    3     6\n\nARRAYS = \n1 4\n2 5\n3 6\n\nDAYMONTH = 12 01\nSTRINGLIST = 'a,b,c'\nFLOATLIST = 1.00 2.00 3.00\nINTLIST = 1 2 3\nDATELIST = \n2021-01-01\n2021-01-02\nSTRING = 'string'\nDECIMAL2F = 1.00\nDECIMAL3F = 1.000\nDECIMAL4F = 1.0000"

    assert (
        model.model_string() == expected_output
    ), f"Expected: \n {expected_output} \n but got \n {model.model_string()}"


def test_table_update():
    table = crp.CROPROTATION.create(
        {
            "CROPSTART": ["2000-04-01"],
            "CROPEND": ["2000-10-31"],
            "CROPFIL": ["'maizes'"],
            "CROPTYPE": [1],
        }
    )

    # Test if method runs without errors
    crp.CROPROTATION.update(table, {"CROPTYPE": [2]})


if __name__ == "__main__":
    test_table_update()
