"""
## Load legacy model

Create a pySWAP model from a directory containing old SWAP input files. This script contains functionality to traverse a directory indicated by the user, find
the necessary input files, and create a pySWAP model from them. The script is designed to be used as a standalone script, but it can also be imported and used
as a function.
"""

import os
import platform
import re
import io
import pandas as pd

PATH_VARIABLES = {"pathworkpathatmpathcroppathdrain"}

IS_WINDOWS = platform.system() == "Windows"
BASE_PATH = ".\\" if IS_WINDOWS else "./"

# --------------------------- Creating pySWAP model from directory ---------------------------------
def string_to_dataframe(df_string):
    # Remove any leading/trailing whitespace and split into lines
    lines = df_string.strip().split("\n")

    # Extract the header
    header = lines[0].split()

    # Create a StringIO object with the data (excluding the header)
    data = io.StringIO("\n".join(lines[1:]))

    # Read the fixed-width formatted data
    df = pd.read_fwf(data, header=None, names=header)

    return df


def read_key_values_from_file(file_path):
    # Normalize the path to handle './' and './/'
    normalized_path = os.path.normpath(file_path)

    # If the path is relative (doesn't start with '/' or a drive letter),
    # make it absolute based on the current working directory
    if not os.path.isabs(normalized_path):
        normalized_path = os.path.abspath(normalized_path)

    with open(normalized_path) as file:
        content = file.read()

    # Regular expression to capture KEY = VALUE pairs
    pattern = re.compile(r"^\s*(\w+)\s*=\s*([^!]+)?(?:\s*!.*)?$", re.MULTILINE)
    matches = pattern.findall(content)

    # Convert matches to a dictionary, stripping whitespace and handling quotes and backslashes
    return {key.strip(): value.strip() for key, value in matches}
