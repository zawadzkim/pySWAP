import pyswap as ps
from pathlib import Path
from pandas import DataFrame, read_csv


def _make_grassgrowth():

    meta = ps.Metadata(author="John Doe",
                       institution="University of Somewhere",
                       email="john.doe@somewhere.com",
                       project="pySWAP test - grass growth",
                       swap_ver="4.2")

    simset = ps.GeneralSettings(
        tstart='1980-01-01',
        tend='1984-12-31',
        nprintday=1,
        swerror=1,
        swmonth=0,
        period=1,
        swres=0,
        swodat=0,
        swyrvar=0,
        datefix='1984-12-31',
        swcsv=1,
        inlist_csv=['pgrassdm', 'grassdm', 'pmowdm', 'mowdm']
    )

    # %% Meteorology section
    from pyswap import testcase

    meteo_data = ps.MetFile(
        metfil='260.met', content=testcase.load_met('grassgrowth'))

    meteo = ps.Meteorology(
        lat=51.0,
        swetr=0,
        metfile=meteo_data,
        swdivide=1,
        swmetdetail=0,
        swetsine=0,
        swrain=2,
        alt=1.9,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
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
        rdi=10.0,
        rri=1.0,
        rdc=40.0,
        swdmi2rd=1,
        swrdc=0,
        rdctb=grass_rdctb
    )

    grass_ox_stress = ps.OxygenStress(
        swoxygen=1,
        hlim1=0.0,
        hlim2u=1.0,
        hlim2l=-1.0,
        swwrtnonox=1,
        aeratecrit=0.7,
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

    dateharvest = ['1980-05-06', '1980-05-28', '1980-06-24', '1980-07-24', '1980-08-19', '1980-09-17', '1980-10-23', '1981-04-14', '1981-05-19',
                   '1981-06-16', '1981-07-14', '1981-08-05', '1981-09-08', '1981-10-28', '1982-05-11', '1982-06-01', '1982-07-06', '1982-08-10',
                   '1982-10-13', '1983-05-19', '1983-06-15', '1983-07-13', '1983-08-17', '1983-10-28', '1984-05-15', '1984-06-07', '1984-07-05',
                   '1984-08-02', '1984-09-11', '1984-11-07']

    grass_management = ps.GrasslandManagement(
        seqgrazmow=[2, 2, 2, 2, 2, 2, 2, 2, 2,
                    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        swharvest=2,
        dateharvest=dateharvest,
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

    croprotation = ps.plant.CROPROTATION.create({'CROPSTART': ['1980-01-01', '1981-01-01', '1982-01-01', '1983-01-01', '1984-01-01'],
                                                 'CROPEND': ['1980-12-31', '1981-12-31', '1982-12-31', '1983-12-31', '1984-12-31'],
                                                 'CROPFIL': ["'grassd'", "'grassd'", "'grassd'", "'grassd'", "'grassd'"],
                                                 'CROPTYPE': [3, 3, 3, 3, 3]})

    crop = ps.plant.Crop(
        swcrop=1,
        rds=200.0,
        table_croprotation=croprotation,
        cropfiles=[crpgrass]
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
        rsoil=600.0,
        swredu=1,
        cofredbl=0.35,
        rsigni=0.5
    )

    # %% setting soil profile

    soil_profile = ps.soilwater.SOILPROFILE.create(
        {'ISUBLAY': [1, 2, 3, 4, 5, 6, 7, 8, 9],
         'ISOILLAY': [1, 1, 2, 3, 3, 4, 4, 5, 5],
         'HSUBLAY': [5.0, 10.0, 10.0, 5.0, 20.0, 50.0, 20.0, 100.0, 120.0],
         'HCOMP': [1.0, 2.5, 5.0, 5.0, 10.0, 10.0, 20.0, 20.0, 40.0],
         'NCOMP': [5, 4, 2, 1, 2, 5, 1, 5, 3]}
    )
    soil_hydraulic_functions = ps.soilwater.SOILHYDRFUNC.create({
        'ORES': [0.02, 0.02, 0.02, 0.01, 0.01],
        'OSAT': [0.40, 0.40, 0.40, 0.36, 0.36],
        'ALFA': [0.0227, 0.0227, 0.0227, 0.0216, 0.0216],
        'NPAR': [1.548, 1.548, 1.548, 1.540, 1.540],
        'KSATFIT': [9.65, 9.65, 9.65, 13.10, 13.10],
        'LEXP': [-0.983, -0.983, -0.983, -0.520, -0.520],
        'H_ENPR': [0.0, 0.0, 0.0, 0.0, 0.0],
        'KSATEXM': [9.65, 9.65, 9.65, 13.10, 13.10],
        'BDENS': [1300.0, 1300.0, 1300.0, 1300.0, 1300.0]
    })

    soilprofile = ps.SoilProfile(
        swsophy=0,
        table_soilprofile=soil_profile,
        swhyst=0,
        table_soilhydrfunc=soil_hydraulic_functions,
        swmacro=0
    )
    # %% drainage settings

    dra_settings = ps.DraSettings(
        dramet=3,
        swdivd=1,
        cofani=[1.0, 1.0, 1.0, 1.0, 1.0],
        swdislay=0
    )

    flux_table = DataFrame({
        'DATOWL1': ['1980-01-01', '1984-12-31'],
        'LEVEL1': [-60.0, -60.0]
    })

    flux1 = ps.Flux(
        level_number=1,
        drares=750.0,
        infres=2000.0,
        swallo=1,
        l=500.0,
        zbotdr=-55.0,
        swdtyp=2,
        table_datowltb=flux_table
    )

    drainageinfiltrationres = ps.DrainageInfiltrationResitance(
        nrlevs=1,
        swintfl=0,
        list_levelfluxes=[flux1]
    )

    dra_file = ps.DraFile(
        drfil='swap',
        general=dra_settings,
        drainageinfiltrationres=drainageinfiltrationres
    )

    lateral_drainage = ps.Drainage(
        swdra=1,
        drafile=dra_file
    )

    # %% bottom boundary

    gwleveltable_path = Path(__file__).parent.joinpath(
        './data/2-grassgrowth/gwlevel.csv')

    table_gwlevel = read_csv(gwleveltable_path, lineterminator='\n')

    bbc_file = ps.BBCFile(
        swbotb=1,
        table_gwlevel=table_gwlevel
    )

    bottom_boundary = ps.BottomBoundary(
        swbbcfile=1, bbcfile=bbc_file, bbcfil='swap')

    # %% heatflow

    soil_texture = ps.extras.SOILTEXTURES.create({
        'PSAND': [0.68, 0.68, 0.77, 0.86, 0.88],
        'PSILT': [0.27, 0.28, 0.19, 0.08, 0.09],
        'PCLAY': [0.05, 0.04, 0.04, 0.06, 0.03],
        'ORGMAT': [0.113, 0.053, 0.018, 0.019, 0.011]
    })

    soil_init_t = ps.extras.INITSOILTEMP.create({
        'ZH': [-10.0, -40.0, -70.0, -95.0],
        'TSOIL': [15.0, 12.0, 10.0, 9.0],
    })

    heat_flow = ps.HeatFlow(
        swhea=1,
        swcalt=2,
        swtopbhea=1,
        swbotbhea=1,
        table_initsoil=soil_init_t,
        table_soiltextures=soil_texture
    )

    # %% model setup
    model = ps.Model(
        metadata=meta,
        general_settings=simset,
        meteorology=meteo,
        crop=crop,
        heatflow=heat_flow,
        soilmoisture=soilmoisture,
        surfaceflow=surfaceflow,
        evaporation=evaporation,
        soilprofile=soilprofile,
        lateraldrainage=lateral_drainage,
        bottomboundary=bottom_boundary
    )

    return model
