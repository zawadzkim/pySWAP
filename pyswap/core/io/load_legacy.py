"""
## Load legacy model

Create a pySWAP model from a directory containing old SWAP input files. This script contains functionality to traverse a directory indicated by the user, find
the necessary input files, and create a pySWAP model from them. The script is designed to be used as a standalone script, but it can also be imported and used
as a function.
"""

# %% imports
import time
from pyswap.core.io.io_ascii import open_ascii
from pyswap import testcase, Metadata
import platform
from pyswap.components import GeneralSettings
from pyswap.core.io.old_swap import (
    load_swp,
)

start_time = time.time()

gs = GeneralSettings(swscre=1)

IS_WINDOWS = platform.system() == "Windows"
BASE_PATH = ".\\" if IS_WINDOWS else "./"

hupsel_swp_path = testcase.load_dataset.RESOURCES["hupselbrook"]["swp"]
hupsel_swp = open_ascii(hupsel_swp_path)

meta = Metadata(
    author="John Doe",
    institution="University of Somewhere",
    email="john.doe@somewhere.com",
    project="pySWAP test - hupselbrook",
    swap_ver="4.2",
)

ml = load_swp(hupsel_swp_path, meta)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")
# %%
print(ml.model_string())

# %%
