"""
## Load legacy model

Create a pySWAP model from a directory containing old SWAP input files. This script contains functionality to traverse a directory indicated by the user, find
the necessary input files, and create a pySWAP model from them. The script is designed to be used as a standalone script, but it can also be imported and used
as a function.
"""

# %% imports
import time
from pathlib import Path

from pyswap import testcase
from pyswap.components import Metadata
from pyswap.components.meteorology import metfile_from_csv
from pyswap.core.io.io_ascii import open_ascii
from pyswap.core.loaders import (
    load_swp,
    load_dra,
    load_crp
)
from pyswap.core.io.old_swap import remove_comments, parse_ascii_file, create_table_objects, create_array_objects


# %% test old loading approach
start_time = time.time()

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
from pyswap.core.loaders import _parse_ascii_file
hupsel_dra_path = testcase.load_dataset.RESOURCES["hupselbrook"]["dra"]

dra = load_dra(hupsel_dra_path)


# Start figuring out how to handle the Flux objects. Maybe instead of object list
# I should make it a DataFrame?
# %%

maizes = load_crp(testcase.load_dataset.RESOURCES["hupselbrook"]["maizes"], "fixed", "maizes")

potatod = load_crp(testcase.load_dataset.RESOURCES["hupselbrook"]["potatod"], "wofost", "potatod")

grassd = load_crp(testcase.load_dataset.RESOURCES["hupselbrook"]["grassd"], "grass", "grassd")
# %%

ml.lateraldrainage.drafile = dra
# %%
ml.crop.cropfiles.update({"maizes": maizes,
                          "potatod": potatod,
                          "grassd": grassd})
# %%
ml.meteorology
# %%
metfile = metfile_from_csv("hupselbrook.met", testcase.load_dataset.RESOURCES["hupselbrook"]["met"])
# %%
ml.meteorology.metfile = metfile
ml.generalsettings.swerror = 1

result = ml.run()
# %%
import inspect
import pandas as pd
from pyswap.components import tables
from pyswap.core.basemodel import BaseTableModel

def member_conditions(member):
    cond = (inspect.isclass(member) and 
            not issubclass(member, pd.Series) and 
            member is not BaseTableModel)
    return cond

members = inspect.getmembers(tables, member_conditions)

members_with_columns = [{"name": v[0], "class": v[1], "cols": tuple(v[1].to_schema().columns.keys())} for v in members]
# %% Checking creation of the extensions
from pyswap.components.simsettings import GeneralSettings

gs = GeneralSettings()
extens = ["csv", "csv_tz", "wba"]

gs.extensions = extens

print(gs.model_string())

# %%
