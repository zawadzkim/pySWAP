import pyswap as psp


def _make_simple_test_model():
    # Generate empty model instance
    ml = psp.Model()

    # Metadata
    meta = psp.components.Metadata(
        author="markvdbrink",
        institution="Wageningen University",
        email="mark.vandenbrink@wur.nl",
        project="02_DrainageDevelopment",
        swap_ver="4.2",
    )
    ml.metadata = meta

    # General model settings
    simset = psp.components.simsettings.GeneralSettings(
        swscre=1,  # Print simulation progression
        swerror=1,  # Print error messages
        tstart="2000-01-01",
        tend="2000-12-31",
        nprintday=1,  # number of output times a day
        swmonth=1,  # monthly output
        # period=1,  # daily output, swmonth=0
        swyrvar=0,  # specify output for .bal and .blc file, unnecessary buth required by SWAP
        datefix="31 12",  # specify output for .bal and .blc file, unnecessary buth required by SWAP
        extensions=["csv", "csv_tz"],  # type of output files
        inlist_csv=[
            "watbal",
            "etterms",
            "crop",
        ],  # check SWAPtools for more options
        inlist_csv_tz=["wc", "h", "o2top", "rwu"],
    )
    ml.generalsettings = simset

    richardsettings = psp.components.simsettings.RichardsSettings(
        swkmean=1,  # Use weighted mean of hydraulic conductivity
        swkimpl=0,  # Do not update hydraulic conductivity within iteration
        dtmin=1e-6,  # minimum time step [d]
        dtmax=0.04,  # maximum time step [d]
        gwlconv=100.0,  # Maximum difference of groundwater level between iterations [cm]
        critdevh1cp=1e-3,  # Maximum relative difference in pressure heads per compartment
        critdevh2cp=1e-2,  # Maximum absolute difference in pressure heads per compartment
        critdevponddt=1e-4,  # Maximum water balance error of ponding layer [cm]
        maxit=30,  # Maximum number of iterations
        maxbacktr=5,  # Maximum number of backtracking cycles within an iteration cycle
    )
    ml.richardsettings = richardsettings

    # Meteorology
    ## metfile
    metfile = psp.components.meteorology.metfile_from_knmi(
        metfil="260.met",
        stations=["260"],
        start="2000-01-01",
        end="2000-12-31",
    )

    meteo = psp.components.meteorology.Meteorology(
        metfile=metfile,
        lat=52.0,
        alt=2,  # [m]
        altw=2.0,  # altitude of wind measurements [m]
        swetr=0,  # Use Penman-Monteith, not ETref
        angstroma=0.25,  # Angstrom coefficient a (Allen et al, 1998)
        angstromb=0.50,  # Angstrom coefficient b (Allen et al, 1998)
        swmetdetail=0,  # daily data
        swdivide=1,  # divide E and T using PM
        swrain=0,  # Use only daily rainfall amounts, not intensity TODO
        swetsine=0,  # Do not distribute Tp and Ep over the day using a sine wave
    )

    ml.meteorology = meteo

    # Initial soil moisture content
    soilmoisture = psp.components.soilwater.SoilMoisture(
        swinco=2,  # Initial soil moisture in static equilibirum with initial groundwater level
        gwli=-85.0,  # Initial groundwater level [cm]
    )
    ml.soilmoisture = soilmoisture

    # Surface flow
    surfaceflow = psp.components.soilwater.SurfaceFlow(
        swrunon=0,  # No runon
        swpondmx=0,  # Constant ponding threshold
        pondmx=0.2,  # Minimum ponding thickness for runoff to occur [cm]
        rsro=0.5,  # resistance to runoff [d]
        rsroexp=1.0,  # exponent of drainage equation for runoff
    )
    ml.surfaceflow = surfaceflow

    # Soil evaporation
    evaporation = psp.components.soilwater.Evaporation(
        swcfbs=0,  # Do not use soil factor to calculate Epot from ETref, unneccesary but required by SWAP
        swredu=2,  # Darcy + Boesten/Stroosnijder for reduction potential soil evaporation top layer
        cofredbo=0.54,  # Reduction factor Boesten/Stroosnijder for potential soil evaporation
        rsoil=150.0,  # Minimum soil resistance to evaporation [s/m]
    )
    ml.evaporation = evaporation

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

    # Bottom boundary condition
    bottom_boundary = psp.components.boundary.BottomBoundary(
        swbbcfile=0,  # Do not specify in separate file
        swbotb=6,  # Bottom flux equals zero
    )
    ml.bottomboundary = bottom_boundary

    # Crop settings
    ## Crop preparation settings
    maize_prep = psp.components.crop.Preparation(
        swprep=0, swsow=0, swgerm=0, dvsend=3.0, swharv=0
    )

    ## Crop development settings
    dvs = [0.0, 0.3, 0.5, 0.7, 1.0, 1.4, 2.0]

    ## Crop height
    maize_chtb = psp.components.crop.CHTB.create(
        {
            "DVS": dvs,
            "CH": [1.0, 15.0, 40.0, 140.0, 170.0, 180.0, 175.0],
        }
    )

    ## Root density as function of depth
    maize_rdctb = psp.components.crop.RDCTB.create(
        {
            "RRD": [0.0, 1.0],
            "RDENS": [1.0, 0.0],
        }
    )

    ### Get WOFOST parameters for maize from database
    db_wofost = psp.db.WOFOSTCropDB()
    maize_wofostparams = db_wofost.load_crop_file("maize").get_variety(
        "Grain_maize_201"
    )

    ### Define other parameters
    maize_cropdev_settings = psp.components.crop.CropDevelopmentSettingsWOFOST(
        # Wofost parameters for maize
        wofost_variety=maize_wofostparams,
        # Evaporation parameters
        swcf=2,  # Use crop height
        chtb=maize_chtb,
        albedo=0.2,  # Albedo of the crop
        rsc=167.0,  # Minimum canopy resistance [s/m]
        rsw=0.0,  # Canopy resistance of intercepted water [s/m]
        # Initial values
        laiem=0.04836,  # LAI at emergence [m2/m2]
        # Green surface area
        ssa=0.0,  # Specific leaf area [ha/kg]
        # Assimilation
        kdif=0.6,  # Extinction coefficient for diffuse light
        kdir=0.75,  # Extinction coefficient for direct light
        eff=0.45,  # Light use efficiency [ka/ha/hr/(J m2 s)]
        # Root development
        rdc=100.0,  # Maximum root depth [cm]
        swrd=2,  # Root depth depends on maximum daily increase
        swdmi2rd=0,  # Rooting depth increase depends on assimilate availability
        rdctb=maize_rdctb,
    )

    ### Get parameters from WOFOST database
    maize_cropdev_settings.update_from_wofost()

    ## Test update function -> validation is triggered
    maize_cropdev_settings = maize_cropdev_settings.update({"RSC": 0.0})

    ## Oxygen stress
    maize_ox_stress = psp.components.crop.OxygenStress(
        swoxygen=1,  # Feddes stress function
        swwrtnonox=0,  # Do not stop root development when anaerobic conditions occur
        hlim1=-15.0,  # no RWU at higher h
        hlim2u=-30.0,  # optimal RWU at lower h, upper layer
        hlim2l=-30.0,  # optimal RWU at lower h, lower layer
    )

    ## Drought stress
    maize_dr_stress = psp.components.crop.DroughtStress(
        swdrought=1,  # Feddes stress function
        hlim3h=-325.0,  # h below which RWU reduction starts at high Tpot
        hlim3l=-600.0,  # h below which RWU reduction starts at low Tpot
        hlim4=-8000.0,  # No RWU at h below this value
        adcrh=0.5,  # High Tpot [cm]
        adcrl=0.1,  # Low Tpot [cm]
    )

    ## Interception
    maize_interception = psp.components.crop.Interception(
        swinter=1,  # method for agricultural crops
        cofab=0.25,  # max interception amount [cm]
    )

    ## Maize crop file
    crpmaize = psp.components.crop.CropFile(
        name="maizes",
        prep=maize_prep,
        cropdev_settings=maize_cropdev_settings,
        oxygenstress=maize_ox_stress,
        droughtstress=maize_dr_stress,
        interception=maize_interception,
    )

    ## Crop rotation
    croprotation = psp.components.crop.CROPROTATION.create(
        {
            "CROPSTART": ["2000-05-01"],
            "CROPEND": ["2000-10-15"],
            "CROPFIL": ["'maizes'"],
            "CROPTYPE": [2],
        }
    )

    # ## No irrigation
    # irrigation = psp.components.crop.Irrigation(
    #     swirr=0,  # No irrigation
    # )

    ## Final crop file
    crop = psp.components.crop.Crop(
        swcrop=1,  # Simulate crop
        rds=40.0,  # Maximum rooting depth [cm]
        croprotation=croprotation,
        cropfiles={"maizes": crpmaize},
    )
    ml.crop = crop

    # Lateral drainage
    ## Freeboard over time
    datowltb1 = psp.components.drainage.DATOWLTB1.create(
        {
            "DATOWL1": ["2000-01-01", "2000-12-31"],
            "LEVEL1": [-80.0, -80.0],
        }
    )

    ## Drainage flux
    flux = psp.components.drainage.Flux(
        drares1=100,  # d
        infres1=1e5,  # d
        swallo1=3,  # only drainage is allowed
        l1=50.0,  # drain spacing [m], to allow for vertical distribution
        zbotdr1=-85.0,  # bottom of drainage medium [cm]
        swdtyp1=2,  # type is open channel
        datowltb1=datowltb1,  # drainage level
    )

    ## Drainage file
    dra = psp.components.drainage.DraFile(
        dramet=3,  # Use resistance
        swdivd=1,  # Calculate vertical distribution of drainage flux
        cofani=[1.0, 1.0],  # anisotropy factor
        swdislay=0,  # No adjustment top layer
        nrlevs=1,  # Number of levels
        swtopnrsrf=0,  # No adjustment bottom discharge layer
        swintfl=0,  # No interflow in highest drainage level
        fluxes=flux,
    )

    # Drainage defition
    drainage = psp.components.drainage.Drainage(
        swdra=1,  # Simulate drainage with basic routine
        drafile=dra,
    )
    ml.lateraldrainage = drainage

    # Heat flow
    # Soil textures for each physical layer
    soiltextures = psp.components.transport.SOILTEXTURES.create(
        {
            "PSAND": [0.87, 0.89],
            "PSILT": [0.1, 0.08],
            "PCLAY": [0.03, 0.03],
            "ORGMAT": [0.057, 0.022],
        }
    )

    # Initial soil temperatures; source: WWL
    initsoiltemp = psp.components.transport.INITSOILTEMP.create(
        {
            "ZH": [-10.0, -40.0, -70.0, -95.0],
            "TSOIL": [12.0, 12.0, 10.0, 9.0],
        }
    )

    heatflow = psp.components.transport.HeatFlow(
        swhea=1,  # Simulate heat flow in soil
        swcalt=2,  # Use the numerical method
        swtopbhea=1,  # Air temperature is top boundary condition
        swbotbhea=1,  # No heat flux in bottom boundary
        initsoiltemp=initsoiltemp,
        soiltextures=soiltextures,
    )
    ml.heatflow = heatflow

    return ml


if __name__ == "__main__":
    ml = _make_simple_test_model()
    ml.run()
