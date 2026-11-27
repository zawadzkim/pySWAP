from pyswap.core.io.io_ascii import open_ascii


def test_open_ascii_reads_plain_ascii(tmp_path):
    path = tmp_path / "swap.swp"
    path.write_bytes(b"  SWCSV = 1   ! comment\n")
    assert open_ascii(path) == "  SWCSV = 1   ! comment\n"


def test_open_ascii_reads_utf8(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("Temperature in °C\n", encoding="utf-8")
    assert open_ascii(path) == "Temperature in °C\n"


def test_open_ascii_falls_back_to_latin1(tmp_path):
    # SWAP writes the .vap header with a Latin-1 "º" (byte 0xBA)
    path = tmp_path / "result.vap"
    path.write_bytes(b"* temperature [\xbaC]\n")
    assert open_ascii(path) == "* temperature [ºC]\n"


def test_open_ascii_reads_empty_file(tmp_path):
    path = tmp_path / "empty.wrn"
    path.write_bytes(b"")
    assert open_ascii(path) == ""
