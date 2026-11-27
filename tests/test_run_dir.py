from pyswap import testcase


def test_run_dir_keeps_inputs_and_outputs(tmp_path):
    run_dir = tmp_path / "hupselbrook"
    model = testcase.get("hupselbrook")
    result = model.run(run_dir=run_dir, silence_warnings=True)

    assert result.csv is not None
    assert not result.csv.empty
    files = {f.name for f in run_dir.iterdir()}
    assert "swap.swp" in files
    assert any(name.endswith(".met") for name in files)
    assert f"{model.generalsettings.outfil}_output.csv" in files
    assert any(name.endswith(".log") for name in files)


def test_default_run_leaves_no_files(tmp_path):
    testcase.get("hupselbrook").run(tmp_path, silence_warnings=True)
    assert list(tmp_path.iterdir()) == []
