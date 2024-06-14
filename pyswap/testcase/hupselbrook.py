from datetime import date as dt
from pandas import DataFrame
from pyswap.simsettings import Metadata, GeneralSettings
from pyswap.atmosphere import Meteorology, load_from_csv
from pyswap.plant import (Preparation, OxygenStress, DroughtStress,
                          Interception, CropDevelopmentSettingsFixed, CropDevelopmentSettingsWOFOST)
from pyswap.plant import CropFile, Crop
from pyswap.irrigation import Irrigation, FixedIrrigation
from pyswap.soilwater import (
    SoilMoisture, SurfaceFlow, Evaporation, SoilProfile)
from pyswap.drainage import Drainage
from pyswap.drainage import DraFile
from pyswap.boundary.boundary import BottomBoundary
from pyswap.model import Model
from pathlib import Path
from pyswap.drainage.drafile import DraSettings, DrainageFormula


def _make_hupselbrook():
    # %% Basic settings of the model

    meta = Metadata(author="John Doe",
                    institution="University of Somewhere",
                    email="john.doe@somewhere.com",
                    project="pySWAP test - hupsel brook",
                    swap_ver="4.2")

    simset = GeneralSettings(
        tstart='2002-01-01',
        tend='2004-12-31',
        nprintday=1,
        swmonth=1,
        swyrvar=0,
        datefix='2004-12-31',
        swvap=1,
        swblc=1,
        swsba=1,
        swinc=1,
        swcsv=1,
        inlist_csv=['pond', 'watbal']
    )

    # %% Meteorology section

    # Obtain the meteorological data from KNMI
    # meteo_data = load_from_knmi(stations='283')
    # load the meteorological data from a cscv file
    metfil_path = Path(__file__).parent.joinpath('./data/hupsel_meteo.met')
    meteo_data = load_from_csv(metfil_path, comment='*')

    meteo = Meteorology(
        metfil='283.met',
        lat=52.0,
        swetr=0,
        meteodata=meteo_data,
        swdivide=1,
        swmetdetail=0,
        alt=10.0,
        altw=10.0,
        angstroma=0.25,
        angstromb=0.5,
    )

    # %% Creating the .crp file for maize (fixed crop)

    prep = Preparation(
        swprep=0,
        swsow=0,
        swgerm=0,
        dvsend=3.0,
        swharv=0
    )
    df_dvs_lai = DataFrame({
        'dvs': [0.0, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0],
        'lai': [0.05, 0.14, 0.61, 4.10, 5.00, 5.80, 5.20]
    })

    df_dvs_ch = DataFrame({
        'dvs': [0.0, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0],
        'ch': [1.0, 15.0, 40.0, 140.0, 170.0, 180.0, 175.0]
    })

    df_dvs_rd = DataFrame({
        'dvs': [0.0, 0.3, 0.5, 0.7, 1.0, 2.0],
        'rd': [5.0, 20.0, 50.0, 80.0, 90.0, 100.0]
    })

    df_rrd_rdens = DataFrame({
        'rrd': [0.0, 1.0],
        'rdens': [1.0, 0.0]
    })

    cropdev_settings = CropDevelopmentSettingsFixed(
        idev=1,
        lcc=168,
        kdif=0.6,
        kdir=0.75,
        swgc=1,
        gctb=df_dvs_lai,
        swcf=2,
        table_dvs_ch=df_dvs_ch,
        albedo=0.23,
        rsc=61.0,
        rsw=0.0,
        swrd=1,
        rdtb=df_dvs_rd,
        rdctb=df_rrd_rdens
    )

    ox_stress = OxygenStress(
        swoxygen=1,
        swwrtnonox=0,
        aeratecrit=0.5,
        hlim1=-15.0,
        hlim2u=-30.0,
        hlim2l=-30.0,
    )

    dr_stress = DroughtStress(
        swdrought=1,
        hlim3h=-325.0,
        hlim3l=-600.0,
        hlim4=-8000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    # serves both, Fixed crop and WOFOST
    interception = Interception(
        swinter=1,
        cofab=0.25
    )

    crpmaize = CropFile(
        name='maizes',
        prep=prep,
        cropdev_settings=cropdev_settings,
        oxygenstress=ox_stress,
        droughtstress=dr_stress,
        interception=interception
    )

    # %% Creating .crp file for potato (WOFOST)

    potato_prep = Preparation(
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

    df_dvs_ch = DataFrame({
        'dvs': [0.0, 1.0, 2.0],
        'ch': [1.0, 40.0, 50.0,]
    })

    dtsmtb = DataFrame({
        'tav': [0.0, 2.0, 13.0, 30.0],
        'dtsm': [0.0, 0.0, 11.0, 28.0]
    })

    slatb = DataFrame({
        'dvs': [0.0, 1.1, 2.0],
        '7sla': [0.0030, 0.0030, 0.0015]
    })

    amaxtb = DataFrame({
        'dvs': [0.0, 1.57, 2.0],
        'amax': [30.0, 30.0, 0.0]
    })

    tmpftb = DataFrame({
        'tavd': [0.0, 3.0, 10.0, 15.0, 20.0, 26.0, 33.0],
        'tmpf': [0.01, 0.01, 0.75, 1.00, 1.00, 0.75, 0.01]
    })

    tmnftb = DataFrame({
        'tmnr': [0.0, 3.0],
        'tmnf': [0.0, 1.0]
    })

    rfsetb = DataFrame({
        'dvs': [0.0, 2.0],
        'rfse': [1.0, 1.0]
    })

    frtb = DataFrame({
        'dvs': [0.00, 1.00, 1.36, 2.00],
        'fr': [0.2, 0.2, 0.0, 0.0]
    })

    fltb = DataFrame({
        'dvs': [0.00, 1.00, 1.27, 1.36, 2.00],
        'fl': [0.8, 0.8, 0.0, 0.0, 0.0]
    })

    fstb = DataFrame({
        'dvs': [0.00, 1.00, 1.27, 1.36, 2.00],
        'fs': [0.20, 0.20, 0.25, 0.00, 0.00]
    })

    fotb = DataFrame({
        'dvs': [0.00, 1.00, 1.27, 1.36, 2.00],
        'fo': [0.00, 0.00, 0.75, 1.00, 1.00]
    })

    rdrrtb = DataFrame({
        'dvs': [0.0000, 1.5000, 1.5001, 2.0000],
        'rdrr': [0.00, 0.00, 0.02, 0.02]
    })

    rdrstb = DataFrame({
        'dvs': [0.0000, 1.5000, 1.5001, 2.0000],
        'rdrs': [0.00, 0.00, 0.02, 0.02]
    })

    rdctb = DataFrame({
        'rrd': [0.0, 1.0],
        'rdens': [1.0, 0.0]
    })

    potato_cropdev_settings = CropDevelopmentSettingsWOFOST(
        swcf=2,
        table_dvs_ch=df_dvs_ch,
        albedo=0.19,
        rsc=207.0,
        rsw=0.0,
        idsl=0,
        tsumea=150.0,
        tsumam=1550.0,
        dtsmtb=dtsmtb,
        tdwi=75.0,
        laiem=0.0589,
        rgrlai=0.012,
        spa=0.0,
        ssa=0.0,
        span=37.0,
        tbase=2.0,
        slatb=slatb,
        kdif=1.0,
        kdir=0.75,
        eff=0.45,
        amaxtb=amaxtb,
        tmpftb=tmpftb,
        tmnftb=tmnftb,
        cvl=0.72,
        cvo=0.85,
        cvr=0.72,
        cvs=0.69,
        q10=2.0,
        rml=0.03,
        rmo=0.0045,
        rmr=0.01,
        rms=0.015,
        rfsetb=rfsetb,
        frtb=frtb,
        fltb=fltb,
        fstb=fstb,
        fotb=fotb,
        perdl=0.03,
        swrd=2,
        rdi=10.0,
        rri=1.2,
        rdc=50.0,
        swdmi2rd=1,
        rdctb=rdctb,
        rdrstb=rdrstb,
        rdrrtb=rdrrtb
    )

    potato_ox_stress = OxygenStress(
        swoxygen=1,
        swwrtnonox=1,
        aeratecrit=0.5,
        hlim1=-10.0,
        hlim2u=-25.0,
        hlim2l=-25.0,
        swrootradius=2,
        root_radiuso2=0.00015
    )

    potato_dr_stress = DroughtStress(
        swdrought=1,
        hlim3h=-300.0,
        hlim3l=-500.0,
        hlim4=-10000.0,
        adcrh=0.5,
        adcrl=0.1,
    )

    crppotato = CropFile(
        name='potatod',
        prep=potato_prep,
        cropdev_settings=potato_cropdev_settings,
        oxygenstress=potato_ox_stress,
        droughtstress=potato_dr_stress,
        # shared with the fixed crop settings
        interception=interception
    )

    # %% Creating the main Crop object

    croprotation = DataFrame({'cropstart': [dt(2002, 5, 1), dt(2003, 5, 10), dt(2004, 1, 1)],
                              'cropend': [dt(2002, 10, 15), dt(2003, 9, 29), dt(2004, 12, 31)],
                              'cropfil': ["'maizes'", "'potatod'", "'grassd'"],
                              'croptype': [1, 2, 3]})

    crp_grass = Path(__file__).parent.joinpath('./data/hupsel_grassd.crp')

    crop_grassd = CropFile(name='grassd', path=str(crp_grass))

    crop = Crop(
        swcrop=1,
        rds=200.0,
        table_croprotation=croprotation,
        cropfiles=[crpmaize, crppotato, crop_grassd]
    )

    # %% irrigation setup

    irrig_events = DataFrame({
        'irdate': ['2002-01-05'],
        'irdepth': [5.0],
        'irconc': [1000.0],
        'irtype': [1]}
    )

    fixed_irrigation = FixedIrrigation(
        swirgfil=0,
        table_irrigevents=irrig_events
    )

    irrigation = Irrigation(
        swirfix=1,
        fixedirrig=fixed_irrigation,
        schedule=0
    )

    # %% Soil moisture setup

    soilmoisture = SoilMoisture(
        swinco=2,
        gwli=-75.0
    )

    # %% surface flow settings

    surfaceflow = SurfaceFlow(
        swpondmx=0,
        pondmx=0.2,
        rsro=0.5,
        rsroexp=1.0,
        swrunon=0
    )

    # %% evaporation settings

    evaporation = Evaporation(
        cfevappond=1.25,
        swcfbs=0,
        rsoil=30.0,
        swredu=1,
        cofredbl=0.35,
        rsigni=0.5
    )

    # %% setting soil profile

    soil_profile = DataFrame(
        {'ISUBLAY': [1, 2, 3, 4],
         'ISOILLAY': [1, 1, 2, 2],
         'HSUBLAY': [10.0, 20.0, 30.0, 140.0],
         'HCOMP': [1.0, 5.0, 5.0, 10.0],
         'NCOMP': [10, 4, 6, 14]}
    )

    soil_hydraulic_functions = DataFrame({
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

    soilprofile = SoilProfile(
        swsophy=0,
        table_soilprofile=soil_profile,
        swhyst=0,
        tau=0.2,
        table_soilhydrfunc=soil_hydraulic_functions,
        swmacro=0
    )

    # %% drainage settings

    dra_settings = DraSettings(
        dramet=2,
        swdivd=1,
        cofani=[1.0, 1.0],
        swdislay=0
    )

    dra_formula = DrainageFormula(
        lm2=11.0,
        shape=0.8,
        wetper=30.0,
        zbotdr=-80.0,
        entres=20.0,
        ipos=2,
        basegw=-200.0,
        khtop=25.0
    )

    dra_file = DraFile(
        name='swap',
        general=dra_settings,
        drainageformula=dra_formula
    )
    # # this is the working solution that just copies the predefined file
    # dra = Path(__file__).parent.joinpath('./data/hupsel_swap.dra')
    # dranage_file = DrainageFile(
    #     name='swap', path=str(dra))

    lateral_drainage = Drainage(
        swdra=1,
        drfil='swap',
        drafile=dra_file
    )

    # %% bottom boundary

    bottom_boundary = BottomBoundary(
        swbbcfile=0,
        swbotb=6
    )

    model = Model(
        metadata=meta,
        simsettings=simset,
        meteorology=meteo,
        crop=crop,
        irrigation=irrigation,
        soilmoisture=soilmoisture,
        surfaceflow=surfaceflow,
        evaporation=evaporation,
        soilprofile=soilprofile,
        lateraldrainage=lateral_drainage,
        bottomboundary=bottom_boundary
    )

    return model
