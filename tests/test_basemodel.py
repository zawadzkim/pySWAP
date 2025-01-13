def test_model_string(simple_model):
    model = simple_model(attr1="test", attr2=12, table_data="1 2 3")
    expected_output = "ATTR1 = test\nATTR2 = 12\n1 2 3"
    assert model.model_string() == expected_output, (
        f"Expected: \n {expected_output} \n but got \n {model.model_string()}"
    )
