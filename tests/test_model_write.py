import pytest

from pyswap import testcase
from pyswap.model.model import ModelBuilder


@pytest.mark.parametrize("case", ["hupselbrook", "grassgrowth"])
def test_write_produces_the_files_run_uses(tmp_path, case):
    model = testcase.get(case)
    written = model.write(tmp_path / "written")
    run_dir = tmp_path / "run"
    model.run(run_dir=run_dir, silence_warnings=True)

    files = sorted(f.name for f in written.iterdir())
    assert "swap.swp" in files
    for name in files:
        assert (run_dir / name).read_bytes() == (written / name).read_bytes(), name


def test_model_builder_still_writes_inputs(tmp_path):
    model = testcase.get("hupselbrook")
    ModelBuilder(model, tmp_path / "builder").write_inputs()
    model.write(tmp_path / "write")
    assert sorted(p.name for p in (tmp_path / "builder").iterdir()) == sorted(
        p.name for p in (tmp_path / "write").iterdir()
    )


def test_to_classic_swap_is_deprecated_but_still_writes(tmp_path):
    model = testcase.get("hupselbrook")
    with pytest.warns(DeprecationWarning, match=r"Model\.write"):
        model.to_classic_swap(tmp_path / "classic")
    model.write(tmp_path / "write")
    assert sorted(p.name for p in (tmp_path / "classic").iterdir()) == sorted(
        p.name for p in (tmp_path / "write").iterdir()
    )
