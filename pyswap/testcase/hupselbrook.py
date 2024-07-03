from datetime import date as dt
import pyswap as ps
from pyswap import testcase


def _make_hupselbrook():
    # %% Basic settings of the model

    meta = ps.Metadata(author="John Doe",
                       institution="University of Somewhere",
                       email="john.doe@somewhere.com",
                       project="pySWAP test - hupselbrook",
                       swap_ver="4.2")

    simset = ps.GeneralSettings(
        tstart='2002-01-01',
        tend='2004-12-31',
        nprintday=1,
        swerror=1,
        swmonth=1,
        swyrvar=0,
        datefix='2004-12-31',
        swvap=1,
        swblc=1,
        swsba=1,
        swinc=1,
        swcsv=1,
        inlist_csv=['rain', 'irrig', 'interc', 'runoff', 'drainage',
                    'dstor', 'epot', 'eact', 'tpot', 'tact', 'qbottom', 'gwl']
    )

    # %% Meteorology section

    meteo_data = ps.MetFile(metfil='283.met',
                            content=testcase.load_met('hupselbrook'))

    meteo = ps.Meteorology(
        lat=52.0,
        swetr=0,
        metfile=meteo_data,
        swdivide=1,
        swmetdetail=0,
        alt=10.0,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
    )

    # %% Creating the .crp file for maize (fixed crop)

    maize_prep = ps.plant.Preparation(
        swprep=0,
        swsow=0,
        swgerm=0,
        dvsend=3.0,
        swharv=0
    )

    scheduled_irrigation = ps.ScheduledIrrigation(
        schedule=0
    )

    DVS = [0.0, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0]

    maize_gctb = ps.plant.GCTB.create({
        'DVS': DVS,
        'LAI': [0.05, 0.14, 0.61, 4.10, 5.00, 5.80, 5.20]
    })

    maize_chtb = ps.plant.CHTB.create({
        'DVS': DVS,
        'CH': [1.0, 15.0, 40.0, 140.0, 170.0, 180.0, 175.0]
    })

    maize_rdtb = ps.plant.RDTB.create({
        'DVS': [0.0, 0.3, 0.5, 0.7, 1.0, 2.0],
        'RD': [5.0, 20.0, 50.0, 80.0, 90.0, 100.0]
    })

    maize_rdctb = ps.plant.RDCTB.create({
        'RRD': [0.0, 1.0],
        'RDENS': [1.0, 0.0]
    })

    maize_cropdev_settings = ps.plant.CropDevelopmentSettingsFixed(
        idev=1,
        lcc=168,
        kdif=0.6,
        kdir=0.75,
        swgc=1,
        gctb=maize_gctb,
        swcf=2,
        table_dvs_ch=maize_chtb,
        albedo=0.23,
        rsc=61.0,
        rsw=0.0,
        swrd=1,
        rdtb=maize_rdtb,
        rdctb=maize_rdctb
    )

    maize_ox_stress = ps.plant.OxygenStress(
        swoxygen=1,
        swwrtnonox=0,
        aeratecrit=0.5,
        hlim1=-15.0,
        hlim2u=-30.0,
        hlim2l=-30.0,
    )

    maize_dr_stress = ps.plant.DroughtStress(
        swdrought=1,
        hlim3h=-325.0,
        hlim3l=-600.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    # serves both, Fixed crop and WOFOST
    maize_interception = ps.plant.Interception(
        swinter=1,
        cofab=0.25
    )

    crpmaize = ps.plant.CropFile(
        name='maizes',
        prep=maize_prep,
        scheduledirrigation=scheduled_irrigation,
        cropdev_settings=maize_cropdev_settings,
        oxygenstress=maize_ox_stress,
        droughtstress=maize_dr_stress,
        interception=maize_interception
    )

    # %% Creating .crp file for potato (WOFOST)

    potato_prep = ps.Preparation(
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
        swharv=0
    )

    potato_chtb = ps.plant.CHTB.create({
        'DVS': [0.0, 1.0, 2.0],
        'CH': [1.0, 40.0, 50.0,]
    })

    potato_dtsmtb = ps.plant.DTSMTB.create({
        'TAV': [0.0, 2.0, 13.0, 30.0],
        'DTSM': [0.0, 0.0, 11.0, 28.0]
    })

    potato_slatb = ps.plant.SLATB.create({
        'DVS': [0.0, 1.1, 2.0],
        'SLA': [0.0030, 0.0030, 0.0015]
    })

    potato_amaxtb = ps.plant.AMAXTB.create({
        'DVS': [0.0, 1.57, 2.0],
        'AMAX': [30.0, 30.0, 0.0]
    })

    potato_tmpftb = ps.plant.TMPFTB.create({
        'tavd': [0.0, 3.0, 10.0, 15.0, 20.0, 26.0, 33.0],
        'tmpf': [0.01, 0.01, 0.75, 1.00, 1.00, 0.75, 0.01]
    })

    potato_tmnftb = ps.plant.TMNFTB.create({
        'TMNR': [0.0, 3.0],
        'TMNF': [0.0, 1.0]
    })

    potato_rfsetb = ps.plant.RFSETB.create({
        'DVS': [0.0, 2.0],
        'RFSE': [1.0, 1.0]
    })

    potato_frtb = ps.plant.FRTB.create({
        'DVS': [0.00, 1.00, 1.36, 2.00],
        'FR': [0.2, 0.2, 0.0, 0.0]
    })

    potato_fltb = ps.plant.FLTB.create({
        'DVS': [0.00, 1.00, 1.27, 1.36, 2.00],
        'FL': [0.8, 0.8, 0.0, 0.0, 0.0]
    })

    potato_fstb = ps.plant.FSTB.create({
        'DVS': [0.00, 1.00, 1.27, 1.36, 2.00],
        'FS': [0.20, 0.20, 0.25, 0.00, 0.00]
    })

    potato_fotb = ps.plant.FOTB.create({
        'DVS': [0.00, 1.00, 1.27, 1.36, 2.00],
        'FO': [0.00, 0.00, 0.75, 1.00, 1.00]
    })

    potato_rdrrtb = ps.plant.RDRRTB.create({
        'DVS': [0.0000, 1.5000, 1.5001, 2.0000],
        'RDRR': [0.00, 0.00, 0.02, 0.02]
    })

    potato_rdrstb = ps.plant.RDRSTB.create({
        'DVS': [0.0000, 1.5000, 1.5001, 2.0000],
        'RDRS': [0.00, 0.00, 0.02, 0.02]
    })

    potato_rdctb = ps.plant.RDCTB.create({
        'RRD': [0.0, 1.0],
        'RDENS': [1.0, 0.0]
    })

    potato_cropdev_settings = ps.CropDevelopmentSettingsWOFOST(
        swcf=2,
        table_dvs_ch=potato_chtb,
        albedo=0.19,
        rsc=207.0,
        rsw=0.0,
        idsl=0,
        tsumea=150.0,
        tsumam=1550.0,
        dtsmtb=potato_dtsmtb,
        tdwi=75.0,
        laiem=0.0589,
        rgrlai=0.012,
        spa=0.0,
        ssa=0.0,
        span=37.0,
        tbase=2.0,
        slatb=potato_slatb,
        kdif=1.0,
        kdir=0.75,
        eff=0.45,
        amaxtb=potato_amaxtb,
        tmpftb=potato_tmpftb,
        tmnftb=potato_tmnftb,
        cvl=0.72,
        cvo=0.85,
        cvr=0.72,
        cvs=0.69,
        q10=2.0,
        rml=0.03,
        rmo=0.0045,
        rmr=0.01,
        rms=0.015,
        rfsetb=potato_rfsetb,
        frtb=potato_frtb,
        fltb=potato_fltb,
        fstb=potato_fstb,
        fotb=potato_fotb,
        perdl=0.03,
        swrd=2,
        rdi=10.0,
        rri=1.2,
        rdc=50.0,
        swdmi2rd=1,
        rdctb=potato_rdctb,
        rdrstb=potato_rdrstb,
        rdrrtb=potato_rdrrtb
    )

    potato_ox_stress = ps.OxygenStress(
        swoxygen=1,
        swwrtnonox=1,
        aeratecrit=0.5,
        hlim1=-10.0,
        hlim2u=-25.0,
        hlim2l=-25.0,
        swrootradius=2,
        root_radiuso2=0.00015
    )

    potato_dr_stress = ps.DroughtStress(
        swdrought=1,
        hlim3h=-300.0,
        hlim3l=-500.0,
        hlim4=-10000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    crppotato = ps.CropFile(
        name='potatod',
        prep=potato_prep,
        cropdev_settings=potato_cropdev_settings,
        oxygenstress=potato_ox_stress,
        droughtstress=potato_dr_stress,
        # shared with the fixed crop settings
        interception=maize_interception,
        scheduledirrigation=scheduled_irrigation
    )

    # %% Grass crp file
    grass_chtb = ps.plant.CHTB_GRASS.create({
        'DNR': [0.0, 180.0, 366.0],
        'CH': [12.0, 12.0, 12.0]
    })

    grass_slatb = ps.plant.SLATB_GRASS.create({
        'DNR': [1.00, 80.00, 300.00, 366.00],
        'SLA': [0.0015, 0.0015, 0.0020, 0.0020]
    })

    amaxtb_grass = ps.plant.AMAXTB_GRASS.create({
        'DNR': [1.00, 95.00, 200.00, 275.00, 366.00],
        'AMAX': [40.00, 40.00, 35.00, 25.00, 25.00]
    })

    grass_tmpftb = ps.plant.TMPFTB.create({
        'TAVD': [0.00, 5.00, 15.00, 25.00, 40.00],
        'TMPF': [0.00, 0.70, 1.00, 1.00, 0.00]
    })
    grass_tmnftb = ps.plant.TMNFTB.create({
        'TMNR': [0.0, 4.0],
        'TMNF': [0.0, 1.0]
    })

    grass_rfsetb = ps.plant.RFSETB_GRASS.create({
        'DNR': [1.00, 366.00],
        'RFSE': [1.0000, 1.0000]
    })

    grass_frtb = ps.plant.FRTB_GRASS.create({
        'DNR': [1.00, 366.00],
        'FR': [0.3000, 0.3000]
    })

    grass_fltb = ps.plant.FLTB_GRASS.create({
        'DNR': [1.00, 366.00],
        'FL': [0.6000, 0.6000]
    })

    grass_fstb = ps.plant.FSTB_GRASS.create({
        'DNR': [1.00, 366.00],
        'FS': [0.4000, 0.4000]
    })

    grass_rdrrtb = ps.plant.RDRRTB_GRASS.create({
        'DNR': [1.0, 180.0, 366.0],
        'RDRR': [0.0, 0.02, 0.02]
    })

    grass_rdrstb = ps.plant.RDRSTB_GRASS.create({
        'DNR': [1.0, 180.0, 366.0],
        'RDRS': [0.0, 0.02, 0.02]
    })

    grass_rlwtb = ps.plant.RLWTB.create({
        'RW': [300.00, 2500.00],
        'RL': [20.0, 40.0]
    })

    grass_rdctb = ps.plant.RDCTB.create({
        'RRD': [0.0, 1.0],
        'RDENS': [1.0, 0.0]
    })

    grass_settings = ps.plant.CropDevelopmentSettingsGrass(
        swcf=2,
        table_dvs_ch=grass_chtb,
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
        amaxtb=amaxtb_grass,
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
        rdctb=grass_rdctb
    )

    grass_ox_stress = ps.OxygenStress(
        swoxygen=1,
        hlim1=0.0,
        hlim2u=1.0,
        hlim2l=-1.0,
        swwrtnonox=0
    )

    grass_drought_stress = ps.DroughtStress(
        swdrought=1,
        swjarvis=4,
        alphcrit=0.7,
        hlim3h=-200.0,
        hlim3l=-800.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1
    )

    grass_salt_stress = ps.SaltStress(
        swsalinity=0
    )

    grass_interception = ps.Interception(
        swinter=1,
        cofab=0.25
    )

    grass_co2 = ps.CO2Correction(
        swco2=0
    )

    grass_dmmowtb = ps.plant.DMMOWTB.create({
        'DNR': [120.0, 152.0, 182.0, 213.0, 366.0],
        'DMMOW': [4700.0, 3700.0, 3200.0, 2700.0, 2700.0]
    })

    grass_dmmowdelay = ps.plant.DMMOWDELAY.create({
        'DMMOWDELAY': [0.0, 2000.0, 4000.0],
        'DAYDELAY': [2, 3, 4]
    })

    grass_management = ps.GrasslandManagement(
        seqgrazmow=[2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        swharvest=1,
        swdmmow=2,
        dmmowtb=grass_dmmowtb,
        maxdaymow=42,
        swlossmow=0,
        mowrest=700.0,
        table_dmmowdelay=grass_dmmowdelay,
        swpotrelmf=1,
        relmf=0.90
    )

    grass_irrigation = ps.ScheduledIrrigation(schedule=0)

    crpgrass = ps.plant.CropFile(
        name='grassd',
        cropdev_settings=grass_settings,
        oxygenstress=grass_ox_stress,
        droughtstress=grass_drought_stress,
        saltstress=grass_salt_stress,
        interception=grass_interception,
        co2correction=grass_co2,
        grasslandmanagement=grass_management,
        scheduledirrigation=grass_irrigation
    )

    # %% Creating the main Crop object

    croprotation = ps.plant.CROPROTATION.create({'CROPSTART': [dt(2002, 5, 1), dt(2003, 5, 10), dt(2004, 1, 1)],
                                                 'CROPEND': [dt(2002, 10, 15), dt(2003, 9, 29), dt(2004, 12, 31)],
                                                 'CROPFIL': ["'maizes'", "'potatod'", "'grassd'"],
                                                 'CROPTYPE': [1, 2, 3]})

    crop = ps.plant.Crop(
        swcrop=1,
        rds=200.0,
        table_croprotation=croprotation,
        cropfiles=[crpmaize, crppotato, crpgrass]
    )

    # %% irrigation setup

    irrig_events = ps.irrigation.IRRIGATION.create({
        'IRDATE': ['2002-01-05'],
        'IRDEPTH': [5.0],
        'IRCONC': [1000.0],
        'IRTYPE': [1]}
    )

    fixed_irrigation = ps.FixedIrrigation(
        swirfix=1,
        swirgfil=0,
        table_irrigevents=irrig_events
    )

    # %% Soil moisture setup

    soilmoisture = ps.SoilMoisture(
        swinco=2,
        gwli=-75.0
    )

    # %% surface flow settings

    surfaceflow = ps.SurfaceFlow(
        swpondmx=0,
        pondmx=0.2,
        rsro=0.5,
        rsroexp=1.0,
        swrunon=0
    )

    # %% evaporation settings

    evaporation = ps.Evaporation(
        cfevappond=1.25,
        swcfbs=0,
        rsoil=30.0,
        swredu=1,
        cofredbl=0.35,
        rsigni=0.5
    )

    # %% setting soil profile

    soil_profile = ps.soilwater.SOILPROFILE.create(
        {'ISUBLAY': [1, 2, 3, 4],
         'ISOILLAY': [1, 1, 2, 2],
         'HSUBLAY': [10.0, 20.0, 30.0, 140.0],
         'HCOMP': [1.0, 5.0, 5.0, 10.0],
         'NCOMP': [10, 4, 6, 14]}
    )

    soil_hydraulic_functions = ps.soilwater.SOILHYDRFUNC.create({
        'ORES': [0.01, 0.02],
        'OSAT': [0.42, 0.38],
        'ALFA': [0.0276, 0.0213],
        'NPAR': [1.491, 1.951],
        'KSATFIT': [12.52, 12.68],
        'LEXP': [-1.060, 0.168],
        'ALFAW': [0.0542, 0.0426],
        'H_ENPR': [0.0, 0.0],
        'KSATEXM': [12.52, 12.68],
        'BDENS': [1315.0, 1315.0]
    })

    soilprofile = ps.SoilProfile(
        swsophy=0,
        table_soilprofile=soil_profile,
        swhyst=0,
        tau=0.2,
        table_soilhydrfunc=soil_hydraulic_functions,
        swmacro=0
    )

    # %% drainage settings

    dra_settings = ps.DraSettings(
        dramet=2,
        swdivd=1,
        cofani=[1.0, 1.0],
        swdislay=0
    )

    dra_formula = ps.DrainageFormula(
        lm2=11.0,
        shape=0.8,
        wetper=30.0,
        zbotdr=-80.0,
        entres=20.0,
        ipos=2,
        basegw=-200.0,
        khtop=25.0
    )

    dra_file = ps.DraFile(
        drfil='swap',
        general=dra_settings,
        drainageformula=dra_formula
    )

    lateral_drainage = ps.Drainage(
        swdra=1,
        drafile=dra_file
    )

    # %% bottom boundary

    bottom_boundary = ps.BottomBoundary(
        swbbcfile=0,
        swbotb=6
    )

    model = ps.Model(
        metadata=meta,
        general_settings=simset,
        meteorology=meteo,
        crop=crop,
        fixedirrigation=fixed_irrigation,
        soilmoisture=soilmoisture,
        surfaceflow=surfaceflow,
        evaporation=evaporation,
        soilprofile=soilprofile,
        lateraldrainage=lateral_drainage,
        bottomboundary=bottom_boundary
    )

    return model
