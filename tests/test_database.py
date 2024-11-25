from pyswap import testcase, HDF5


def test_database():
    f = HDF5(filename="data.h5")

    # Create instances of the model and result
    model = testcase.get("hupselbrook")
    model2 = model.model_copy(
        update={"version": "v2", "crop": model.crop.model_copy(update={"rds": 195})}
    )
    model3 = model.model_copy(
        update={"version": "v3", "crop": model.crop.model_copy(update={"rds": 100})}
    )
    result = model.run("./")
    result2 = model.run("./")
    result3 = model.run("./")

    # Save to HDF5
    f.save_model(
        model=model, result=result, overwrite_datasets=True, overwrite_project=True
    )
    f.save_model(model=model2, result=result2, overwrite_datasets=True)
    f.save_model(model=model3, result=result3, overwrite_datasets=True)

    # Load from HDF5
    f.load("pySWAP test - hupsel brook", load_results=True)

    print(f.models["base"][1].output[["TACT", "TPOT"]].resample("YE").sum())
    print(f.models["v2"][1].output[["TACT", "TPOT"]].resample("YE").sum())
    print(f.models["v3"][1].output[["TACT", "TPOT"]].resample("YE").sum())