import logging
import shutil

from pyswap import Model, testcase
from pyswap.components.metadata import Metadata

GRASSGROWTH_FILES = ["swap.swp", "swap.bbc", "swap.dra", "260.met", "grassd.crp"]


def _grassgrowth_dir(tmp_path):
    """A copy of the classic SWAP input files of the grassgrowth case."""
    source = testcase.get_path("grassgrowth", "swp").parent
    folder = tmp_path / "grassgrowth"
    folder.mkdir()
    for name in GRASSGROWTH_FILES:
        shutil.copy(source / name, folder)
    return folder


def test_load_then_write_reproduces_the_inputs(tmp_path):
    """Loading the bundled grassgrowth case from its .swp and writing it gives
    the same files as the testcase assembled with the individual loaders."""
    reference = testcase.get("grassgrowth")
    loaded = Model.load(
        _grassgrowth_dir(tmp_path) / "swap.swp", metadata=reference.metadata
    )

    assert set(loaded.crop.cropfiles) == {"grassd"}
    assert loaded.lateraldrainage.drafile is not None
    assert loaded.meteorology.metfile is not None

    expected = reference.write(tmp_path / "expected")
    written = loaded.write(tmp_path / "written")
    names = sorted(f.name for f in expected.iterdir())
    assert names == sorted(f.name for f in written.iterdir())
    for name in names:
        assert (written / name).read_bytes() == (expected / name).read_bytes(), name


def test_load_without_metadata_takes_project_from_swp(tmp_path):
    loaded = Model.load(_grassgrowth_dir(tmp_path) / "swap.swp")
    assert isinstance(loaded.metadata, Metadata)
    assert loaded.metadata.project == "ruurlo"


def test_load_warns_about_missing_files(tmp_path, caplog):
    folder = _grassgrowth_dir(tmp_path)
    (folder / "260.met").unlink()
    with caplog.at_level(logging.WARNING):
        loaded = Model.load(folder / "swap.swp")
    assert loaded.meteorology.metfile is None
    assert "260.met" in caplog.text
