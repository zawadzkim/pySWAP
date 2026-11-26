import logging
import shutil

from pyswap import Model, load_irg, load_met, testcase
from pyswap.components.irrigation import FixedIrrigation
from pyswap.components.metadata import Metadata

GRASSGROWTH_FILES = ["swap.swp", "swap.bbc", "swap.dra", "260.met", "grassd.crp"]


def _grassgrowth_dir_source():
    return testcase.get_path("grassgrowth", "swp").parent


def _grassgrowth_dir(tmp_path):
    """A copy of the classic SWAP input files of the grassgrowth case."""
    source = _grassgrowth_dir_source()
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


def test_load_met_reads_yearly_files():
    """The macropore testcase ships old-style yearly files: whitespace
    separated, a "*" units line after the header, header case differing
    between years."""
    folder = testcase.get_path("macroporeflow", "met").parent
    metfile = load_met([folder / "andelst_meteo.998", folder / "andelst_meteo.999"])

    assert metfile.metfil == "andelst_meteo.met"
    assert len(metfile.content) == 365 + 116
    assert not metfile.content.isna().any().any()
    assert list(metfile.content.YYYY.astype(int).unique()) == [1998, 1999]
    assert metfile.content.STATION.iloc[0] == "'ANDE-M'"


def test_load_met_reads_a_met_file_like_the_testcase():
    folder = _grassgrowth_dir_source()
    reference = testcase.get("grassgrowth").meteorology.metfile
    metfile = load_met(folder / "260.met")
    assert metfile.metfil == "260.met"
    assert metfile.content.to_csv(index=False) == reference.content.to_csv(index=False)


def test_load_reads_yearly_met_files(tmp_path):
    """METFIL without extension: Model.load reads <METFIL>.yyy for each year
    of the simulation and merges them into <METFIL>.met."""
    folder = _grassgrowth_dir(tmp_path)
    met = (folder / "260.met").read_text().splitlines()
    header = next(line for line in met if line.startswith("Station"))
    rows = [line for line in met if line.startswith("'")]
    for year in range(1980, 1985):
        lines = [
            "* yearly weather file",
            " ".join(header.split(",")),
            "* units",
            "",
            *(" ".join(r.split(",")) for r in rows if r.split(",")[3] == str(year)),
        ]
        (folder / f"ruurlo.{year % 1000:03d}").write_text("\n".join(lines) + "\n")
    (folder / "260.met").unlink()
    swp = folder / "swap.swp"
    swp.write_text(swp.read_text().replace("METFIL = '260.met'", "METFIL = 'ruurlo'"))

    loaded = Model.load(swp)

    reference = testcase.get("grassgrowth").meteorology.metfile.content
    assert loaded.meteorology.metfile.metfil == "ruurlo.met"
    assert loaded.meteorology.metfile.content.to_csv(index=False) == reference.to_csv(
        index=False
    )


def test_load_warns_about_a_missing_yearly_file(tmp_path, caplog):
    folder = _grassgrowth_dir(tmp_path)
    swp = folder / "swap.swp"
    swp.write_text(swp.read_text().replace("METFIL = '260.met'", "METFIL = 'ruurlo'"))
    with caplog.at_level(logging.WARNING):
        loaded = Model.load(swp)
    assert loaded.meteorology.metfile is None
    assert "ruurlo.980" in caplog.text


def test_load_reads_the_irrigation_file(tmp_path):
    """A model with fixed irrigation in a separate .irg file gives the same
    .swp and .irg after a write, load, write round trip. (Crop files are left
    out: load_crp does not reproduce them byte for byte.)"""
    model = testcase.get("hupselbrook")
    model.fixedirrigation = FixedIrrigation(
        swirfix=1, swirgfil=1, irrigevents=model.fixedirrigation.irrigevents
    )
    first = model.write(tmp_path / "first")
    assert (first / "swap.irg").exists()

    loaded = Model.load(first / "swap.swp", metadata=model.metadata)
    assert loaded.fixedirrigation.swirgfil == 1
    second = loaded.write(tmp_path / "second")

    for name in ["swap.swp", "swap.irg"]:
        assert (second / name).read_bytes() == (first / name).read_bytes(), name
    # the loaded .met header is upper case; SWAP reads the columns by position
    assert (second / "283.met").read_text().lower() == (
        first / "283.met"
    ).read_text().lower()


def test_load_irg_returns_fixed_irrigation(tmp_path):
    model = testcase.get("hupselbrook")
    model.fixedirrigation = FixedIrrigation(
        swirfix=1, swirgfil=1, irrigevents=model.fixedirrigation.irrigevents
    )
    model.fixedirrigation.write_irg(tmp_path)

    irrigation = load_irg(tmp_path / "swap.irg")
    assert irrigation.swirgfil == 1
    assert irrigation.irg == model.fixedirrigation.irg
