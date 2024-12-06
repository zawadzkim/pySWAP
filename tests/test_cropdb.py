# %%
from pyswap.core.db import WOFOSTCropDB
import pyswap


db = WOFOSTCropDB()
db.croptypes

 # %%

potato = db.load_crop_file("potato")
potato.varieties

# %%

potato_params = potato.get_variety("Potato_701")

# %%

scheduled_irrigation = pyswap.components.irrigation.ScheduledIrrigation(schedule=0)

potato_prep = pyswap.components.crop.Preparation(
    swprep=0,
    swsow=0,
    swgerm=2,
    tsumemeopt=170.0,
    tbasem=3.0,
    teffmx=18.0,
    hdrygerm=-500.0,
    hwetgerm=-100.0,
    zgerm=-10.0,
    agerm=203.0,
    dvsend=2.0,
    swharv=0,
)

potato_chtb = pyswap.CHTB.create({
    "DVS": [0.0, 1.0, 2.0],
    "CH": [
        1.0,
        40.0,
        50.0,
    ],
})

potato_rdctb = pyswap.RDCTB.create({"RRD": [0.0, 1.0], "RDENS": [1.0, 0.0]})

# This is Potato_701 variety from wofost crop file
potato_cropdev_settings = pyswap.components.crop.CropDevelopmentSettingsWOFOST(
    wofost_variety=potato_params,
    swcf=2,
    dvs_ch=potato_chtb,
    albedo=0.19,
    rsc=207.0,
    rsw=0.0,
    ssa=0.0,
    kdir=0.75,
    eff=0.45,  # Available as table EFFTB (SSA/DVS) in potato.yaml
    swrd=2,
    rdc=50.0,
    swdmi2rd=1,
    rdctb=potato_rdctb
)

potato_cropdev_settings

# %%

# potato_ox_stress = pyswap.components.crop.OxygenStress(
#     swoxygen=1,
#     swwrtnonox=1,
#     aeratecrit=0.5,
#     hlim1=-10.0,
#     hlim2u=-25.0,
#     hlim2l=-25.0,
#     swrootradius=2,
#     root_radiuso2=0.00015,
# )

# potato_dr_stress = pyswap.components.crop.DroughtStress(
#     swdrought=1,
#     hlim3h=-300.0,
#     hlim3l=-500.0,
#     hlim4=-10000.0,
#     adcrh=0.5,
#     adcrl=0.1,
# )

# crppotato = pyswap.components.crop.CropFile(
#     name="potatod",
#     prep=potato_prep,
#     cropdev_settings=potato_cropdev_settings,
#     oxygenstress=potato_ox_stress,
#     droughtstress=potato_dr_stress,
#     # shared with the fixed crop settings
#     interception=maize_interception,
#     scheduledirrigation=scheduled_irrigation,
# )