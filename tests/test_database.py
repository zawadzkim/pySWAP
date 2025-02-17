# mypy: disable-error-code="index"
from pyswap import testcase
from pyswap.db import HDF5


def test_database():
    f = HDF5(filename="data.h5")

    # Create instances of the model and result
    model = testcase.get("hupselbrook")
    model2 = model.model_copy(
        update={"version": "v2", "crop": model.crop.model_copy(update={"rds": 195})}
    )

    result = model.run("./")
    result2 = model.run("./")

    # Save to HDF5
    f.save_model(
        model=model, result=result, overwrite_datasets=True, overwrite_project=True
    )
    f.save_model(model=model2, result=result2, overwrite_datasets=True)

    # Load from HDF5
    assert f.list_projects == ["psp test - hupselbrook"]
    assert f.list_models["psp test - hupselbrook"] == ["base", "v2"]
