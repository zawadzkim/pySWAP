# test_read_key_values.py
import os

import pandas as pd
import pytest

from pyswap.io.load_legacy import read_key_values_from_file
from pyswap.io.tables import string_to_dataframe


def test_read_key_values_from_file(sample_file):
    result = read_key_values_from_file(sample_file)

    expected = {
        "PROJECT": "'swap-test'",
        "PATHWORK": "'.\\'",
        "PATHATM": "'.\\'",
        "PATHCROP": "'.\\'",
        "PATHDRAIN": "'.\\'",
        "SWSCRE": "0",
    }

    assert result == expected, f"Expected {expected}, but got {result}"


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_key_values_from_file("non_existent_file.txt")


def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    result = read_key_values_from_file(empty_file)
    assert result == {}, "Expected an empty dictionary for an empty file"


def test_relative_path(sample_file):
    # Change to the directory containing the sample file
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(sample_file))

    try:
        # Test with './'
        result = read_key_values_from_file("./test_sample_input.txt")
        assert result != {}, "Expected non-empty dictionary for relative path './'"

        # Test with './/'
        result = read_key_values_from_file(".//test_sample_input.txt")
        assert result != {}, "Expected non-empty dictionary for relative path '//'"
    finally:
        # Change back to the original directory
        os.chdir(original_dir)


def test_string_to_dataframe():
    original_df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    df_string = original_df.to_string()

    reconstructed_df = string_to_dataframe(df_string)

    assert reconstructed_df.shape == original_df.shape

    assert list(reconstructed_df.columns) == list(original_df.columns)

    pd.testing.assert_frame_equal(reconstructed_df, original_df)

    mixed_df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["a", "b", "c"],
        "C": [1.1, 2.2, 3.3],
    })
    mixed_string = mixed_df.to_string()
    reconstructed_mixed = string_to_dataframe(mixed_string)

    assert reconstructed_mixed.shape == mixed_df.shape

    assert list(reconstructed_mixed.columns) == list(mixed_df.columns)

    pd.testing.assert_frame_equal(reconstructed_mixed, mixed_df, check_dtype=False)
