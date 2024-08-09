from datetime import date as dt
import pyswap as ps
from pathlib import Path
from pandas import DataFrame


def _make_oxygenstress():

    # %% General section
    meta = ps.Metadata(
        author="John Doe",
        institution="University of Somewhere",
        email="john.doe@somewhere.com",
        project="pySWAP test - hupselbrook",
        swap_ver="4.2"
    )

    general = ps.GeneralSettings(
        tstart='1993-01-01',
        tend='2002-12-31',
        swerror=1,
        nprintday=1,
        swmonth=0,
        period=1,
        swres=0,
        swodat=0,
        swyrvar=0,
        datefix='1993-12-31',
        inlist_csv=['pgrassdm', 'grassdm',
                    'pmowdm', 'mowdm', 'treddry', 'tredwet']
    )

    # %% Meteorological section
    metfile = ps.MetFile(
        metfil='260.met',
        content=ps.testcase.load_met('oxygenstress')
    )

    meteo_location = ps.MeteoLocation(
        lat=52.1,
        alt=1.9,
    )

    meteo = ps.Meteorology(
        meteo_location=meteo_location,
        swetr=0,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
        swdivide=1,
        swmetdetail=0,
        swetsine=0,
        swrain=2,
        metfile=metfile
    )

    # %% Crop section
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

        swrd=2,
        rdi=10.00,
        rri=1.00,
        rdc=40.0,

        swdmi2rd=1,
        swrdc=0,
        rdctb=grass_rdctb
    )

    grass_ox_stress = ps.OxygenStress(
        swoxygen=2,
        q10_microbial=2.8,
        specific_resp_humus=1.6e-3,
        srl=383571.0,
        swrootradius=2,
        root_radiuso2=0.000075,
        swwrtnonox=1,
        aeratecrit=0.5,
    )

    grass_drought_stress = ps.DroughtStress(
        swdrought=1,
        hlim3h=-200.0,
        hlim3l=-800.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1
    )

    grass_salt_stress = ps.SaltStress(
        swsalinity=0
    )

    grass_rwu_comp = ps.CompensateRWUStress(
        swcompensate=1,
        swstressor=1,
        alphacrit=0.7,
        dcritrtz=16
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
        scheduledirrigation=grass_irrigation,
        compensaterwu=grass_rwu_comp
    )

    crop_rotation = ps.plant.CROPROTATION.create(
        {'cropstart': ['1993-01-01', '1994-01-01', '1995-01-01',
                       '1996-01-01', '1997-01-01', '1998-01-01',
                       '1999-01-01', '2000-01-01', '2001-01-01', '2002-01-01'],
         'cropend': ['1993-12-31', '1994-12-31', '1995-12-31',
                     '1996-12-31', '1997-12-31', '1998-12-31',
                     '1999-12-31', '2000-12-31', '2001-12-31', '2002-12-31'],
         'cropfil': ["'grassd'", "'grassd'", "'grassd'", "'grassd'", "'grassd'",
                     "'grassd'", "'grassd'", "'grassd'", "'grassd'", "'grassd'",],
         'croptype': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]}
    )

    crop = ps.Crop(
        swcrop=1,
        rds=200.0,
        table_croprotation=crop_rotation,
        cropfiles=[crpgrass]
    )

    # %% soil water section

    soil_moisture = ps.SoilMoisture(
        swinco=2,
        gwli=-15.0,
    )

    surface_flow = ps.SurfaceFlow(
        swpondmx=0,
        pondmx=0.2,
        rsro=0.5,
        rsroexp=1.0,
        swrunon=0
    )

    evaporation = ps.Evaporation(
        cfevappond=1.25,
        swcfbs=0,
        rsoil=600.0,
        swredu=1,
        cofredbl=0.35,
        rsigni=0.5
    )

    soil_profile = ps.soilwater.SOILPROFILE.create(
        {
            'isublay': [1, 2, 3, 4, 5, 6, 7, 8],
            'isoillay': [1, 1, 2, 3, 4, 4, 4, 4],
            'hsublay': [5.0, 20.0, 15.0, 35.0, 15.0, 110.0, 100.0, 100.0],
            'hcomp': [1.0, 2.5, 5.0,  5.0,  7.5, 10.0, 20.0, 25.0],
            'ncomp': [5, 8, 3, 7, 2, 11, 5, 4]
        }
    )

    soil_hydr_func = ps.soilwater.SOILHYDRFUNC.create(
        {
            'ores': [0.1, 0.0, 0.0, 0.0],
            'osat': [0.722, 0.830, 0.902, 0.900],
            'alfa': [0.0305, 0.0121, 0.0177, 0.0158],
            'npar': [1.124, 1.108, 1.349, 1.361],
            'ksatfit': [5.8, 1.7, 1.7, 2.4],
            'lexp': [0.000, -4.884, -3.410, -2.861],
            'h_enpr': [0.0, 0.0, 0.0, 0.0],
            'ksatexm': [5.8, 1.7, 1.7, 2.4],
            'bdens': [557.0, 222.0, 194.0, 137.0]
        }
    )

    soil = ps.SoilProfile(
        swsophy=0,
        swhyst=0,
        table_soilprofile=soil_profile,
        table_soilhydrfunc=soil_hydr_func,
        swmacro=0
    )

    # %% Drainage section
    dra_settings = ps.DraSettings(
        dramet=3,
        swdivd=1,
        cofani=[1.0, 1.0, 1.0, 1.0],
        swdislay=0
    )
    table_datowltb1 = DataFrame({
        'DATOWL1': ['1993-01-01', '2002-12-31'],
        'LEVEL1': [-21.3, -21.3]
    })

    flux1 = ps.Flux(
        level_number=1,
        drares=130.0,
        infres=150.0,
        swallo=1,
        l=40.0,
        zbotdr=-140.0,
        swdtyp=2,
        table_datowltb=table_datowltb1)

    table_datowltb2 = DataFrame({
        'DATOWL2': ['1993-01-01', '2002-12-31'],
        'LEVEL2': [-20.0, -20.0]
    })

    flux2 = ps.Flux(
        level_number=2,
        drares=50.0,
        infres=40.0,
        swallo=3,
        l=15.0,
        zbotdr=-20.0,
        swdtyp=2,
        table_datowltb=table_datowltb2
    )

    inf_res = ps.DrainageInfRes(
        nrlevs=2,
        swintfl=0,
        list_levelfluxes=[flux1, flux2]
    )

    drafile = ps.DraFile(
        general=dra_settings,
        drfil='swap',
        drainageinfres=inf_res
    )

    lateral_drainage = ps.Drainage(swdra=1, drafile=drafile)

    # %% bottom boundary

    haquiftb = DataFrame({
        'DATE3': ['1993-01-01', '1993-03-15', '1993-04-15',
                  '1993-06-15', '1993-07-15', '1993-09-15',
                  '1993-10-15', '1993-12-15', '1994-01-15',
                  '1994-03-16', '1994-04-16', '1994-06-16',
                  '1994-07-16', '1994-09-16', '1994-10-16',
                  '1994-12-16', '1995-01-01', '1995-03-15',
                  '1995-04-15', '1995-06-15', '1995-07-15',
                  '1995-09-15', '1995-10-15', '1995-12-15',
                  '1996-01-15', '1996-03-15', '1996-04-15',
                  '1996-06-15', '1996-07-15', '1996-09-15',
                  '1996-10-15', '1996-12-15', '1997-01-01',
                  '1997-03-15', '1997-04-15', '1997-06-15',
                  '1997-07-15', '1997-09-15', '1997-10-15',
                  '1997-12-15', '1998-01-15', '1998-03-16',
                  '1998-04-16', '1998-06-16', '1998-07-16',
                  '1998-09-16', '1998-10-16', '1998-12-16',
                  '1999-01-01', '1999-03-15', '1999-04-15',
                  '1999-06-15', '1999-07-15', '1999-09-15',
                  '1999-10-15', '1999-12-15', '2000-01-15',
                  '2000-03-15', '2000-04-15', '2000-06-15',
                  '2000-07-15', '2000-09-15', '2000-10-15',
                  '2000-12-15', '2001-01-01', '2001-03-15',
                  '2001-04-15', '2001-06-15', '2001-07-15',
                  '2001-09-15', '2001-10-15', '2001-12-15',
                  '2002-01-15', '2002-03-16', '2002-04-16',
                  '2002-06-16', '2002-07-16', '2002-09-16',
                  '2002-10-16', '2002-12-31'],
        'HAQUIF': [-36.66, -36.66, -57.47, -57.47, -60.11,
                   -60.11, -46.70, -46.70, -36.66, -36.66,
                   -57.47, -57.47, -60.11, -60.11, -46.70,
                   -46.70, -36.66, -36.66, -57.47, -57.47,
                   -60.11, -60.11, -46.70, -46.70, -36.66,
                   -36.66, -57.47, -57.47, -60.11, -60.11,
                   -46.70, -46.70, -36.66, -36.66, -57.47,
                   -57.47, -60.11, -60.11, -46.70, -46.70,
                   -36.66, -36.66, -57.47, -57.47, -60.11,
                   -60.11, -46.70, -46.70, -36.66, -36.66,
                   -57.47, -57.47, -60.11, -60.11, -46.70,
                   -46.70, -36.66, -36.66, -57.47, -57.47,
                   -60.11, -60.11, -46.70, -46.70, -36.66,
                   -36.66, -57.47, -57.47, -60.11, -60.11,
                   -46.70, -46.70, -36.66, -36.66, -57.47,
                   -57.47, -60.11, -60.11, -46.70, -46.70]
    })
    bottom_boundary = ps.BottomBoundary(
        swbbcfile=0,
        swbotb=3,
        swbotb3resvert=0,
        swbotb3impl=1,
        shape=1.0,
        hdrain=-25.0,
        rimlay=500.0,
        sw3=2,
        sw4=0,
        table_haquif=haquiftb
    )

    # %% heat flow

    physical_soil = ps.extras.SOILTEXTURES.create(
        {
            'psand': [0.699, 0.658, 0.217, 0.000],
            'psilt': [0.108, 0.138, 0.528, 0.373],
            'pclay': [0.193, 0.204, 0.254, 0.627],
            'orgmat': [0.192, 0.181, 0.341, 0.777]
        }
    )

    init_soil_temp = ps.extras.INITSOILTEMP.create(
        {
            'ZH': [0.0, -30.0, -298.0],
            'TSOIL': [7.0, 10.0, 10.0]
        }
    )

    heat_flow = ps.HeatFlow(
        swhea=1,
        swcalt=2,
        swtopbhea=1,
        swbotbhea=1,
        table_soiltextures=physical_soil,
        table_initsoil=init_soil_temp
    )
    # %% main model part

    model = ps.Model(
        metadata=meta,
        general_settings=general,
        meteorology=meteo,
        crop=crop,
        fixedirrigation=ps.FixedIrrigation(swirfix=0),
        soilmoisture=soil_moisture,
        surfaceflow=surface_flow,
        evaporation=evaporation,
        soilprofile=soil,
        lateraldrainage=lateral_drainage,
        bottomboundary=bottom_boundary,
        heatflow=heat_flow
    )

    return model
