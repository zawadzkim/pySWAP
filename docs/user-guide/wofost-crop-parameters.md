# WOFOST crop parameters

pySWAP includes the WOFOST crop parameter sets maintained by Allard de Wit (Wageningen Environmental Research) in the [WOFOST_crop_parameters](https://github.com/ajwdewit/WOFOST_crop_parameters) repository. A copy is bundled as a git submodule in `pyswap/libs/WOFOST_crop_parameters`, and `psp.db.WOFOSTCropDB` reads it (see the [WOFOST crop database tutorial](../tutorials/notebooks/003-wofost-crop-db.ipynb)).

## Where the parameters apply

Each parameter set was calibrated for particular varieties, regions and management. pySWAP does not restrict or adjust them; the repository documents where each set comes from, and the same information is in the metadata of every crop file and variety:

```python
import pyswap as psp

potato = psp.db.WOFOSTCropDB().load_crop_file("potato")
variety = potato.get_variety("Potato_701")
variety.metadata["Description"]  # how and where the variety was calibrated
variety.metadata["Coverage"]  # region
variety.metadata["Source"]  # reference
```

Use a parameter set as a starting point. Check that its variety, region and growing conditions match your site, and calibrate your own parameters if they do not.

The first time a crop file is loaded in a session, pySWAP shows a warning pointing to the repository.
