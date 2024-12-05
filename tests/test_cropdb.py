# %%
from pyswap.core.db import WOFOSTCropDB


db = WOFOSTCropDB()
db.croptypes

 # %%

potato = db.load_crop_file("potato")
potato.varieties

# %%

potato_params = potato.get_variety("Potato_701")
potato_meta = potato.get_variety("Potato_701", what="metadata")
potato_meta = potato.get_variety("Potato_701", what="all")


print(potato_params)
print(potato_meta)

# %%

formatted = potato.format_tables(potato_params)

# %%
