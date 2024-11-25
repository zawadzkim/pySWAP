import os
import re
import platform

PATH_VARIABLES = {
    "pathwork"
    "pathatm"
    "pathcrop"
    "pathdrain"
}

IS_WINDOWS = platform.system() == "Windows"
BASE_PATH = ".\\" if IS_WINDOWS else "./"

def read_key_values_from_file(file_path):
    
    # Normalize the path to handle './' and './/'
    normalized_path = os.path.normpath(file_path)
    
    # If the path is relative (doesn't start with '/' or a drive letter), 
    # make it absolute based on the current working directory
    if not os.path.isabs(normalized_path):
        normalized_path = os.path.abspath(normalized_path)
    
    with open(normalized_path, 'r') as file:
        content = file.read()
    
    # Regular expression to capture KEY = VALUE pairs
    pattern = re.compile(r'^\s*(\w+)\s*=\s*([^!]+)?(?:\s*!.*)?$', re.MULTILINE)
    matches = pattern.findall(content)
    
    # Convert matches to a dictionary, stripping whitespace and handling quotes and backslashes
    return {
        key.strip(): value.strip()
        for key, value in matches
    }