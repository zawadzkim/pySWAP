# %%
from datetime import date as dt

import pyswap as psp
from pyswap import testcase
from pyswap.db import WOFOSTCropDB

# %%


def _make_hupselbrook():
    # %% Basic settings of the model

    ml = psp.Model()

    meta = psp.components.Metadata(
        author="John Doe",
        institution="University of Somewhere",
        email="john.doe@somewhere.com",
        project="psp test - hupselbrook",
        swap_ver="4.2",
    )

    ml.metadata = meta

    simset = psp.components.simsettings.GeneralSettings(
        tstart="2002-01-01",
        tend="2004-12-31",
        extensions=["vap", "blc", "sba", "inc", "csv"],
        nprintday=1,
        swerror=1,
        swscre=0,
        swmonth=1,
        swyrvar=0,
        datefix="31 12",
        inlist_csv=[
            "rain",
            "irrig",
            "interc",
            "runoff",
            "drainage",
            "dstor",
            "epot",
            "eact",
            "tpot",
            "tact",
            "qbottom",
            "gwl",
        ],
    )

    ml.generalsettings = simset

    # %% Meteorology section

    meteo_location = psp.gis.Location(lat=52.0, lon=21.0, alt=10.0)

    meteo_data = psp.components.meteorology.MetFile(
        metfil="283.met", content=testcase.load_met("hupselbrook")
    )

    meteo = psp.components.meteorology.Meteorology(
        meteo_location=meteo_location,
        swetr=0,
        metfile=meteo_data,
        swdivide=1,
        swmetdetail=0,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
    )

    ml.meteorology = meteo

    # %% Creating the .crp file for maize (fixed crop)

    maize_prep = psp.components.crop.Preparation(
        swprep=0, swsow=0, swgerm=0, dvsend=3.0, swharv=0
    )

    scheduled_irrigation = psp.components.irrigation.ScheduledIrrigation(schedule=0)

    DVS = [0.0, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0]

    maize_gctb = psp.components.crop.GCTB.create(
        {
            "DVS": DVS,
            "LAI": [0.05, 0.14, 0.61, 4.10, 5.00, 5.80, 5.20],
        }
    )

    maize_chtb = psp.components.crop.CHTB.create(
        {
            "DVS": DVS,
            "CH": [1.0, 15.0, 40.0, 140.0, 170.0, 180.0, 175.0],
        }
    )

    maize_rdtb = psp.components.crop.RDTB.create(
        {
            "DVS": [0.0, 0.3, 0.5, 0.7, 1.0, 2.0],
            "RD": [5.0, 20.0, 50.0, 80.0, 90.0, 100.0],
        }
    )

    maize_rdctb = psp.components.crop.RDCTB.create(
        {
            "RRD": [0.0, 1.0],
            "RDENS": [1.0, 0.0],
        }
    )

    maize_cropdev_settings = psp.components.crop.CropDevelopmentSettingsFixed(
        idev=1,
        lcc=168,
        kdif=0.6,
        kdir=0.75,
        swgc=1,
        gctb=maize_gctb,
        swcf=2,
        chtb=maize_chtb,
        albedo=0.23,
        rsc=61.0,
        rsw=0.0,
        swrd=1,
        rdtb=maize_rdtb,
        rdctb=maize_rdctb,
    )

    maize_ox_stress = psp.components.crop.OxygenStress(
        swoxygen=1,
        swwrtnonox=0,
        aeratecrit=0.5,
        hlim1=-15.0,
        hlim2u=-30.0,
        hlim2l=-30.0,
    )

    maize_dr_stress = psp.components.crop.DroughtStress(
        swdrought=1,
        hlim3h=-325.0,
        hlim3l=-600.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    # serves both, Fixed crop and WOFOST
    maize_interception = psp.components.crop.Interception(swinter=1, cofab=0.25)

    crpmaize = psp.components.crop.CropFile(
        name="maizes",
        prep=maize_prep,
        scheduledirrigation=scheduled_irrigation,
        cropdev_settings=maize_cropdev_settings,
        oxygenstress=maize_ox_stress,
        droughtstress=maize_dr_stress,
        interception=maize_interception,
    )

    # %% Creating .crp file for potato (WOFOST)

    potato_prep = psp.components.crop.Preparation(
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

    potato_chtb = psp.components.crop.CHTB.create(
        {
            "DVS": [0.0, 1.0, 2.0],
            "CH": [
                1.0,
                40.0,
                50.0,
            ],
        }
    )

    potato_rdctb = psp.components.crop.RDCTB.create(
        {
            "RRD": [0.0, 1.0],
            "RDENS": [1.0, 0.0],
        }
    )

    # Load the crop database
    db = WOFOSTCropDB()
    potato = db.load_crop_file("potato")
    potato_params = potato.get_variety("Potato_701")

    potato_cropdev_settings = psp.components.crop.CropDevelopmentSettingsWOFOST(
        wofost_variety=potato_params,
        swcf=2,
        chtb=potato_chtb,
        idsl=0,
        albedo=0.19,
        laiem=0.0589,
        ssa=0.0,
        kdif=1.0,
        rsc=207.0,
        rsw=0.0,
        kdir=0.75,
        eff=0.45,
        swrd=2,
        rdc=50.0,
        swdmi2rd=1,
        rdctb=potato_rdctb,
    )

    potato_cropdev_settings.update_from_wofost()

    potato_ox_stress = psp.components.crop.OxygenStress(
        swoxygen=1,
        swwrtnonox=1,
        aeratecrit=0.5,
        hlim1=-10.0,
        hlim2u=-25.0,
        hlim2l=-25.0,
        swrootradius=2,
        root_radiuso2=0.00015,
    )

    potato_dr_stress = psp.components.crop.DroughtStress(
        swdrought=1,
        hlim3h=-300.0,
        hlim3l=-500.0,
        hlim4=-10000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    crppotato = psp.components.crop.CropFile(
        name="potatod",
        prep=potato_prep,
        cropdev_settings=potato_cropdev_settings,
        oxygenstress=potato_ox_stress,
        droughtstress=potato_dr_stress,
        # shared with the fixed crop settings
        interception=maize_interception,
        scheduledirrigation=scheduled_irrigation,
    )

    # %% Grass crp file
    grass_chtb = psp.components.crop.CHTB.create(
        {
            "DNR": [0.0, 180.0, 366.0],
            "CH": [12.0, 12.0, 12.0],
        }
    )

    grass_slatb = psp.components.crop.SLATB.create(
        {
            "DNR": [1.00, 80.00, 300.00, 366.00],
            "SLA": [0.0015, 0.0015, 0.0020, 0.0020],
        }
    )

    grass_amaxtb = psp.components.crop.AMAXTB.create(
        {
            "DNR": [1.00, 95.00, 200.00, 275.00, 366.00],
            "AMAX": [40.00, 40.00, 35.00, 25.00, 25.00],
        }
    )

    grass_tmpftb = psp.components.crop.TMPFTB.create(
        {
            "TAVD": [0.00, 5.00, 15.00, 25.00, 40.00],
            "TMPF": [0.00, 0.70, 1.00, 1.00, 0.00],
        }
    )
    grass_tmnftb = psp.components.crop.TMNFTB.create(
        {
            "TMNR": [0.0, 4.0],
            "TMNF": [0.0, 1.0],
        }
    )

    grass_rfsetb = psp.components.crop.RFSETB.create(
        {
            "DNR": [1.00, 366.00],
            "RFSE": [1.0000, 1.0000],
        }
    )

    grass_frtb = psp.components.crop.FRTB.create(
        {
            "DNR": [1.00, 366.00],
            "FR": [0.3000, 0.3000],
        }
    )

    grass_fltb = psp.components.crop.FLTB.create(
        {
            "DNR": [1.00, 366.00],
            "FL": [0.6000, 0.6000],
        }
    )

    grass_fstb = psp.components.crop.FSTB.create(
        {
            "DNR": [1.00, 366.00],
            "FS": [0.4000, 0.4000],
        }
    )

    grass_rdrrtb = psp.components.crop.RDRRTB.create(
        {
            "DNR": [1.0, 180.0, 366.0],
            "RDRR": [0.0, 0.02, 0.02],
        }
    )

    grass_rdrstb = psp.components.crop.RDRSTB.create(
        {
            "DNR": [1.0, 180.0, 366.0],
            "RDRS": [0.0, 0.02, 0.02],
        }
    )

    grass_rlwtb = psp.components.crop.RLWTB.create(
        {
            "RW": [300.00, 2500.00],
            "RL": [20.0, 40.0],
        }
    )

    grass_rdctb = psp.components.crop.RDCTB.create(
        {
            "RRD": [0.0, 1.0],
            "RDENS": [1.0, 0.0],
        }
    )

    grass_settings = psp.components.crop.CropDevelopmentSettingsGrass(
        swcf=2,
        chtb=grass_chtb,
        albedo=0.23,
        rsc=100.0,
        rsw=0.0,
        tdwi=1000.00,
        laiem=0.63000,
        rgrlai=0.00700,
        swtsum=1,
        ssa=0.0004,
        span=30.00,
        tbase=0.00,
        slatb=grass_slatb,
        kdif=0.60,
        kdir=0.75,
        eff=0.50,
        amaxtb=grass_amaxtb,
        tmpftb=grass_tmpftb,
        tmnftb=grass_tmnftb,
        cvl=0.6850,
        cvr=0.6940,
        cvs=0.6620,
        q10=2.0000,
        rml=0.0300,
        rmr=0.0150,
        rms=0.0150,
        rfsetb=grass_rfsetb,
        frtb=grass_frtb,
        fltb=grass_fltb,
        fstb=grass_fstb,
        perdl=0.050,
        rdrrtb=grass_rdrrtb,
        rdrstb=grass_rdrstb,
        swrd=3,
        swdmi2rd=1,
        rlwtb=grass_rlwtb,
        wrtmax=3000.0,
        swrdc=0,
        rdctb=grass_rdctb,
    )

    grass_ox_stress = psp.components.crop.OxygenStress(
        swoxygen=1, hlim1=0.0, hlim2u=1.0, hlim2l=-1.0, swwrtnonox=0
    )

    grass_drought_stress = psp.components.crop.DroughtStress(
        swdrought=1,
        swjarvis=4,
        alphcrit=0.7,
        hlim3h=-200.0,
        hlim3l=-800.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    grass_salt_stress = psp.components.crop.SaltStress(swsalinity=0)

    grass_interception = psp.components.crop.Interception(swinter=1, cofab=0.25)

    grass_co2 = psp.components.crop.CO2Correction(swco2=0)

    grass_dmmowtb = psp.components.crop.DMMOWTB.create(
        {
            "DNR": [120.0, 152.0, 182.0, 213.0, 366.0],
            "DMMOW": [4700.0, 3700.0, 3200.0, 2700.0, 2700.0],
        }
    )

    grass_dmmowdelay = psp.components.crop.DMMOWDELAY.create(
        {
            "DMMOWDELAY": [0.0, 2000.0, 4000.0],
            "DAYDELAY": [2, 3, 4],
        }
    )

    grass_management = psp.components.crop.GrasslandManagement(
        seqgrazmow=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        swharvest=1,
        swdmmow=2,
        dmmowtb=grass_dmmowtb,
        maxdaymow=42,
        swlossmow=0,
        mowrest=700.0,
        dmmowdelay=grass_dmmowdelay,
        swpotrelmf=1,
        relmf=0.90,
    )

    grass_irrigation = psp.components.irrigation.ScheduledIrrigation(schedule=0)

    crpgrass = psp.components.crop.CropFile(
        name="grassd",
        cropdev_settings=grass_settings,
        oxygenstress=grass_ox_stress,
        droughtstress=grass_drought_stress,
        saltstress=grass_salt_stress,
        interception=grass_interception,
        co2correction=grass_co2,
        grasslandmanagement=grass_management,
        scheduledirrigation=grass_irrigation,
    )

    # %% Creating the main Crop object

    croprotation = psp.components.crop.CROPROTATION.create(
        {
            "CROPSTART": [dt(2002, 5, 1), dt(2003, 5, 10), dt(2004, 1, 1)],
            "CROPEND": [dt(2002, 10, 15), dt(2003, 9, 29), dt(2004, 12, 31)],
            "CROPFIL": ["'maizes'", "'potatod'", "'grassd'"],
            "CROPTYPE": [1, 2, 3],
        }
    )

    crop = psp.components.crop.Crop(
        swcrop=1,
        rds=200.0,
        croprotation=croprotation,
        cropfiles={"maizes": crpmaize, "potatod": crppotato, "grassd": crpgrass},
    )

    ml.crop = crop

    # %% irrigation setup

    irrig_events = psp.components.irrigation.IRRIGEVENTS.create(
        {
            "IRDATE": ["2002-01-05"],
            "IRDEPTH": [5.0],
            "IRCONC": [1000.0],
            "IRTYPE": [1],
        }
    )

    fixed_irrigation = psp.components.irrigation.FixedIrrigation(
        swirfix=1, swirgfil=0, irrigevents=irrig_events
    )

    ml.fixedirrigation = fixed_irrigation

    # %% Soil moisture setup

    soilmoisture = psp.components.soilwater.SoilMoisture(swinco=2, gwli=-75.0)
    ml.soilmoisture = soilmoisture

    # %% surface flow settings

    surfaceflow = psp.components.soilwater.SurfaceFlow(
        swpondmx=0, pondmx=0.2, rsro=0.5, rsroexp=1.0, swrunon=0
    )

    ml.surfaceflow = surfaceflow

    # %% evaporation settings

    evaporation = psp.components.soilwater.Evaporation(
        cfevappond=1.25, swcfbs=0, rsoil=30.0, swredu=1, cofredbl=0.35, rsigni=0.5
    )

    ml.evaporation = evaporation

    # %% setting soil profile

    soil_profile = psp.components.soilwater.SOILPROFILE.create(
        {
            "ISUBLAY": [1, 2, 3, 4],
            "ISOILLAY": [1, 1, 2, 2],
            "HSUBLAY": [10.0, 20.0, 30.0, 140.0],
            "HCOMP": [1.0, 5.0, 5.0, 10.0],
            "NCOMP": [10, 4, 6, 14],
        }
    )

    soil_hydraulic_functions = psp.components.soilwater.SOILHYDRFUNC.create(
        {
            "ORES": [0.01, 0.02],
            "OSAT": [0.42, 0.38],
            "ALFA": [0.0276, 0.0213],
            "NPAR": [1.491, 1.951],
            "KSATFIT": [12.52, 12.68],
            "LEXP": [-1.060, 0.168],
            "ALFAW": [0.0542, 0.0426],
            "H_ENPR": [0.0, 0.0],
            "KSATEXM": [12.52, 12.68],
            "BDENS": [1315.0, 1315.0],
        }
    )

    soilprofile = psp.components.soilwater.SoilProfile(
        swsophy=0,
        soilprofile=soil_profile,
        swhyst=0,
        tau=0.2,
        soilhydrfunc=soil_hydraulic_functions,
        swmacro=0,
    )

    ml.soilprofile = soilprofile

    # %% drainage settings

    dra = psp.components.drainage.DraFile(
        dramet=2,
        swdivd=1,
        cofani=[1.0, 1.0],
        swdislay=0,
        lm2=11.0,
        shape=0.8,
        wetper=30.0,
        zbotdr=-80.0,
        entres=20.0,
        ipos=2,
        basegw=-200.0,
        khtop=25.0,
    )
    drainage = psp.components.drainage.Drainage(swdra=1, drafile=dra)

    ml.lateraldrainage = drainage

    # %% bottom boundary

    bottom_boundary = psp.components.boundary.BottomBoundary(swbbcfile=0, swbotb=6)

    ml.bottomboundary = bottom_boundary

    return ml
