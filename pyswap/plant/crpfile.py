"""Create .crp file for SWAP model.

Similar to the .dra or .swp files, the .crp file is a configuration file for the SWAP model. 
The classes in this module represent distincs sections of the .crp file. The main class is the
`CropFile` class which holds the settings for the crop simulation.

Classes:
    CropFile: Class for the .crp file.
    CropDevelopmentSettings: Class for the crop development settings.
    CropDevelopmentSettingsWOFOST: Class for the crop development settings in WOFOST.
    CropDevelopmentSettingsFixed: Class for the fixed crop development settings.
    OxygenStress: Class for the oxygen stress settings.
    DroughtStress: Class for the drought stress settings.
    SaltStress: Class for the salt stress settings.
    CompensateRWUStress: Class for the compensate root water uptake stress settings.
    Interception: Class for the interception settings.
    CO2Correction: Class for the CO2 correction settings.
    ScheduledIrrigation: Class for the scheduled irrigation settings.
    Preparation: Class for the preparation settings.


Warning:
    This script will undergo major changes in the future. Some things to improve include
    smoother integration with WOFOST configuration files (yaml) and code readability.
"""
from pydantic import Field
from ..core import (Table, Arrays, UNITRANGE, DateList, IntList,
                    YEARRANGE, PySWAPBaseModel, open_file)
from ..irrigation import ScheduledIrrigation
from typing import Literal, Optional
from typing_extensions import Self
from pydantic import Field, model_validator, computed_field


class CropDevelopmentSettings(PySWAPBaseModel):
    """Crop development settings (parts 1-xx form the template)

    Note:
        The validation of this class should be optimized. The current implementation
        repeats the validation of the base class in each subclass. The observed issue is that
        when the validator is inherited from the base class and there is another validator in the
        subclass (even if they have different names), at the validation step of the child class the
        validator throws an error that the attribute is NoneType. To be fixed later.

    Attributes:
        swcf (Literal[1, 2]): Choose between crop factor and crop height

            * 1 - Crop factor
            * 2 - Crop height

        table_dvs_cf (Optional[Table]): Table with crop factors as a function of development stage
        table_dvs_ch (Optional[Table]): Table with crop height as a function of development stage
        albedo (Optional[float]): Crop reflection coefficient
        rsc (Optional[float]): Minimum canopy resistance
        rsw (Optional[float]): Canopy resistance of intercepted water
        tsumea (float): Temperature sum from emergence to anthesis
        tsumam (float): Temperature sum from anthesis to maturity
        tbase (Optional[float]): Start value of temperature sum
        kdif (float): Extinction coefficient for diffuse visible light
        kdir (float): Extinction coefficient for direct visible light
        swrd (Optional[Literal[1, 2, 3]]): Switch development of root growth

            * 1 - Root growth depends on development stage
            * 2 - Root growth depends on maximum daily increase
            * 3 - Root growth depends on available root biomass

        rdtb (Optional[Arrays]): Rooting Depth as a function of development stage
        rdi (float): Initial rooting depth
        rri (float): Maximum daily increase in rooting depth
        rdc (float): Maximum rooting depth of particular crop
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth

            * 0 - Rooting depth increase is related to availability assimilates for roots
            * 1 - Rooting depth increase is related to relative dry matter increase

        rlwtb (Optional[Arrays]): rooting depth as function of root weight
        wrtmax (float): Maximum root weight
        swrdc (Literal[0, 1]): Switch for calculation of relative root density
        rdctb (Arrays): root density as function of relative rooting depth
    """
    swcf: Literal[1, 2]
    table_dvs_cf: Optional[Table] = None
    table_dvs_ch: Optional[Table] = None
    albedo: Optional[float] = Field(default=None, **UNITRANGE)
    rsc: Optional[float] = Field(default=None, ge=0.0, le=1.0e6)
    rsw: Optional[float] = Field(default=None, ge=0.0, le=1.0e6)
    # In WOFOST reference yaml files this is called TSUM1
    tsumea: float = Field(default=None, ge=0.0, le=1.0e4)
    # In WOFOST reference yaml files this is called TSUM2
    tsumam: float = Field(default=None, ge=0.0, le=1.0e4)
    # In SWAP this parameter seems to meen something different than in the
    # WOFOST template. The range of value is the same though.
    tbase: Optional[float] = Field(default=None, ge=-10.0, le=30.0)
    kdif: float = Field(ge=0.0, le=2.0)
    kdir: float = Field(ge=0.0, le=2.0)
    swrd: Optional[Literal[1, 2, 3]] = None
    rdtb: Optional[Arrays] = None
    rdi: float = Field(default=None, ge=0.0, le=1000.0)
    rri: float = Field(default=None, ge=0.0, le=100.0)
    rdc: float = Field(default=None, ge=0.0, le=1000.0)
    swdmi2rd: Optional[Literal[0, 1]] = None
    rlwtb: Optional[Arrays] = None
    wrtmax: float = Field(default=None, ge=0.0, le=1.0e5)
    swrdc: Literal[0, 1] = 0
    rdctb: Arrays


class CropDevelopmentSettingsWOFOST(CropDevelopmentSettings):
    """Additional settings for the 

    Warning:
        The validation for this class is not complete. Also check the Optional attributes!

    Note:
        Use serialization_alias to change the parameter names who are different between WOFOST and SWAP.

    Attributes:
        idsl (Literal[0, 1, 2]):
        dtsmtb (Arrays):
        dlo (Optional[float]):
        dlc (Optional[float]):
        vernsat (Optional[float]):
        vernbase (Optional[float]):
        verndvs (Optional[float]):
        verntb (Optional[Arrays]):
        tdwi (float):
        laiem (float):
        rgrlai (float):
        spa (float):
        ssa (float):
        span (float):
        slatb (Arrays):
        eff (float):
        amaxtb (Arrays):
        tmpftb (Arrays):
        tmnftb (Arrays):
        cvo (float):
        cvl (float):
        cvr (float):
        cvs (float):
        q10 (float):
        rml (float):
        rmo (float):
        rmr (float):
        rms (float):
        rfsetb (Arrays):
        frtb (Arrays):
        fltb (Arrays):
        fstb (Arrays):
        fotb (Arrays):
        perdl (float):
        rdrrtb (Arrays):
        rdrstb (Arrays):
    """
    idsl: Optional[Literal[0, 1, 2]] = None  # for grass at least
    dtsmtb: Optional[Arrays] = None   # for grass at least
    dlo: Optional[float] = Field(default=None, ge=0.0, le=24.0)
    dlc: Optional[float] = Field(default=None, ge=0.0, le=24.0)
    vernsat: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    vernbase: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    verndvs: Optional[float] = Field(default=None, ge=0.0, le=0.3)
    verntb: Optional[Arrays] = None
    tdwi: float = Field(ge=0.0, le=10_000)
    laiem: float = Field(ge=0.0, le=10)
    rgrlai: float = Field(**UNITRANGE)
    spa: Optional[float] = Field(**UNITRANGE, default=None)
    ssa: float = Field(**UNITRANGE)
    span: float = Field(**YEARRANGE)
    slatb: Arrays
    eff:  float = Field(ge=0.0, le=10.0)
    amaxtb: Arrays
    tmpftb: Arrays
    tmnftb: Arrays
    cvo: Optional[float] = Field(
        **UNITRANGE, default=None)  # for grass at least
    cvl: float = Field(**UNITRANGE)
    cvr: float = Field(**UNITRANGE)
    cvs: float = Field(**UNITRANGE)
    q10: float = Field(ge=0.0, le=5.0)
    rml: float = Field(**UNITRANGE)
    rmo: Optional[float] = Field(
        **UNITRANGE, default=None)  # for grass at least
    rmr: float = Field(**UNITRANGE)
    rms: float = Field(**UNITRANGE)
    rfsetb: Arrays
    frtb: Arrays
    fltb: Arrays
    fstb: Arrays
    fotb: Optional[Arrays] = None  # for grass at least
    perdl: float = Field(ge=0.0, le=3.0)
    rdrrtb: Arrays
    rdrstb: Arrays

    @model_validator(mode='after')
    def _validate_crop_wofost(self) -> Self:
        # validation of the base class
        if self.swcf == 1:
            assert self.table_dvs_cf is not None, "table_dvs_cf is required when swcf is 1."
        elif self.swcf == 2:
            assert self.table_dvs_ch is not None, "table_dvs_ch is required when swcf is 2."
            assert self.albedo is not None, "albedo is required when swcf is 2."
            assert self.rsc is not None, "rsc is required when swcf is 2."
            assert self.rsw is not None, "rsw is required when swcf is 2."
        if self.swrd == 1:
            assert self.rdtb is not None, "rdtb is required when swrd is 1."
        elif self.swrd == 2:
            assert self.rdi is not None, "rdi is required when swrd is 2."
            assert self.rri is not None, "rri is required when swrd is 2."
            assert self.rdc is not None, "rdc is required when swrd is 2."
            assert self.swdmi2rd is not None, "swdmi2rd is required when swrd is 2."
        elif self.swrd == 3:
            assert self.rlwtb is not None, "rlwtb is required when swrd is 3."
            assert self.wrtmax is not None, "wrtmax is required when swrd is 3."
        # validation specific to the WOFOST crop development settings
        if self.idsl in [1, 2]:
            assert self.dlc is not None, "dlc is required when idsl is either 1 or 2."
            assert self.dlo is not None, "dlo is required when idsl is either 1 or 2."
        elif self.idsl == 2:
            assert self.vernsat is not None, "vernsat is required when idsl is 2."
            assert self.vernbase is not None, "vernbase is required when idsl is 2."
            assert self.verndvs is not None, "verndvs is required when idsl is 2."
            assert self.verntb is not None, "verntb is required when idsl is 2."

        return self


class CropDevelopmentSettingsFixed(CropDevelopmentSettings):
    """Fixed crop development settings (parts 1-xx form the template)

    Warning:
        This class is not complete. It is missing the validation.

    Note:
        I noticed an issue with the tables here. They are actually arrays (each
        array is a column) that are preceeded by the variable name and "=". That variable
        name is the same for all options of tables which have different column names (e.g., DVS/LAI or
        DVS/SCF) but the variable name is the same (e.g., GCTB).
        TODO: implement a check of the column before the df is converted to string.

    Attributes:
        idev (Literal[1, 2]): Duration of crop growing period

            * 1 - Duration is fixed
            * 2 - Duration is variable

        lcc (Optional[int]): Duration of the crop growing period
        swgc (Literal[1, 2]): Choose between Leaf Area Index or Soil Cover Fraction

            * 1 - LAI
            * 2 - SCF

        gctb (Arrays): Soil Cover Fraction as a function of development stage
    """

    idev: Literal[1, 2]
    lcc: Optional[int] = Field(default=None, **YEARRANGE)
    swgc: Literal[1, 2]
    gctb: Arrays
    kytb: Optional[Arrays] = None

    @model_validator(mode='after')
    def _validate_crop_fixed(self) -> Self:
        # validation of the base class
        if self.swcf == 1:
            assert self.table_dvs_cf is not None, "table_dvs_cf is required when swcf is 1."
        elif self.swcf == 2:
            assert self.table_dvs_ch is not None, "table_dvs_ch is required when swcf is 2."
            assert self.albedo is not None, "albedo is required when swcf is 2."
            assert self.rsc is not None, "rsc is required when swcf is 2."
            assert self.rsw is not None, "rsw is required when swcf is 2."
        if self.swrd == 1:
            assert self.rdtb is not None, "rdtb is required when swrd is 1."
        elif self.swrd == 2:
            assert self.rdi is not None, "rdi is required when swrd is 2."
            assert self.rri is not None, "rri is required when swrd is 2."
            assert self.rdc is not None, "rdc is required when swrd is 2."
            assert self.swdmi2rd is not None, "swdmi2rd is required when swrd is 2."
        elif self.swrd == 3:
            assert self.rlwtb is not None, "rlwtb is required when swrd is 3."
            assert self.wrtmax is not None, "wrtmax is required when swrd is 3."
        # validation specific to the fixed crop development settings
        if self.idev == 1:
            assert self.lcc is not None, "lcc is required when idev is 1."
        elif self.idev == 2:
            assert self.tsumea is not None, "tsumea is required when idev is 2."
            assert self.tsumam is not None, "tsumam is required when idev is 2."
            assert self.tbase is not None, "tbase is required when idev is 2."

        return self


class CropDevelopmentSettingsGrass(CropDevelopmentSettingsWOFOST):
    """Crop development settings specific to grass growth.

    Attributes:
        swtsum (Literal[0, 1, 2]): Select either sum air temperatures or soil temperature at particular depth

            * 0 - no delay of start grass growth
            * 1 - start of grass growth based on sum air temperatures > 200 degree C
            * 2 - start of grass growth based on soil temperature at particular depth

        tsumtemp (Optional[float]): Specific stem area [0..1 ha/kg, R]
        tsumdepth (Optional[float]): Life span under leaves under optimum conditions [0..366 d, R]
        tsumtime (Optional[float]): Lower threshold temperature for ageing of leaves [-10..30 degree C, R]
    """
    swtsum: Literal[0, 1, 2]
    tsumtemp: Optional[float] = None
    tsumdepth: Optional[float] = None
    tsumtime: Optional[float] = None


class OxygenStress(PySWAPBaseModel):
    """Oxygen stress settings for .crp file.

    Attributes:
        swoxygen (Literal[0, 1, 2]): Switch for oxygen stress

            * 0 - No oxygen stress
            * 1 - Oxygen stress according to Feddes et al. (1978)
            * 2 - Oxygen stress according to Bartholomeus et al. (2008)

        swoxygentype (Optional[Literal[1, 2]]): switch for physical processes or repro. functions to calculate oxygen stress

            * 1 - physical processes
            * 2 - reproduction functions

        swwrtnonox (Literal[0, 1]): Switch for checking aerobic conditions in root zone to stop root(zone) development
        aeratecrit (Optional[float]): Threshold to stop root extension in case of oxygenstress; 0.0 maximum oxygen stress
        hlim1 (Optional[float]): No water extraction at higher pressure heads
        hlim2u (Optional[float]): H below which optimum water extr. starts for top layer
        hlim2l (Optional[float]): H below which optimum water extr. starts for sub layer
        q10_microbial (Optional[float]): Relative increase in microbial respiration at temperature increase of 10 C
        specific_resp_humus (Optional[float]): Respiration rate of humus at 25 C
        srl (Optional[float]): Specific root length
        swrootradius (Optional[Literal[1, 2]]): Switch for calculation of root radius

            * 1 - Calculate root radius
            * 2 - Root radius given in an input file

        dry_mat_cont_roots (Optional[float]): Dry matter content of roots
        air_filled_root_por (Optional[float]): Air filled root porosity
        spec_weight_root_tissue (Optional[float]): Specific weight of non-airfilled root tissue
        var_a (Optional[float]): Variance of root radius
        root_radiuso2 (Optional[float]): Root radius for oxygen stress module
        q10_root (Optional[float]): Relative increase in root respiration at temperature increase of 10 oC
        f_senes (Optional[float]): Reduction factor for senescence, used for maintenance respiration
        c_mroot (Optional[float]): Maintenance coefficient of root
        table_max_resp_factor (Optional[Table]): Ratio root total respiration / maintenance respiration as a function of development stage
        table_dvs_w_root_ss (Optional[Table]): List dry weight of roots at soil surface as a function of development stage

    TODO: Find a way to validate the parameters that are required when the
    croptype=1 and swoxygen=2 (currently I cannot access the croptype parameter)
    """

    swoxygen: Literal[0, 1, 2]
    swwrtnonox: Literal[0, 1]
    swoxygentype: Optional[Literal[1, 2]] = None
    aeratecrit: Optional[float] = Field(default=None, ge=0.0001, le=1.0)
    hlim1: Optional[float] = Field(default=None, ge=-100.0, le=100.0)
    hlim2u: Optional[float] = Field(default=None, ge=-1000.0, le=100.0)
    hlim2l: Optional[float] = Field(default=None, ge=-1000.0, le=100.0)
    q10_microbial: Optional[float] = Field(default=None, ge=1.0, le=4.0)
    specific_resp_humus: Optional[float] = Field(default=None, **UNITRANGE)
    srl: Optional[float] = Field(default=None, ge=0.0, le=1.0e10)
    swrootradius: Optional[Literal[1, 2]] = None
    dry_mat_cont_roots: Optional[float] = Field(default=None, **UNITRANGE)
    air_filled_root_por: Optional[float] = Field(default=None, **UNITRANGE)
    spec_weight_root_tissue: Optional[float] = Field(
        default=None, ge=0.0, le=1.0e5)
    var_a: Optional[float] = Field(default=None, **UNITRANGE)
    root_radiuso2: Optional[float] = Field(default=None, ge=1.0e-6, le=0.1)
    q10_root: Optional[float] = Field(default=None, ge=1.0, le=4.0)
    f_senes: Optional[float] = Field(default=None, **UNITRANGE)
    c_mroot: Optional[float] = Field(default=None, **UNITRANGE)
    mrftb: Optional[Arrays] = None
    wrtb: Optional[Arrays] = None

    @model_validator(mode='after')
    def _validate_oxygen(self) -> Self:
        if self.swoxygen == 1:
            assert self.hlim1 is not None, "hlim1 is required when swoxygen is 1."
            assert self.hlim2u is not None, "hlim2u is required when swoxygen is 1."
            assert self.hlim2l is not None, "hlim2l is required when swoxygen is 1."
        elif self.swoxygen == 2:
            assert self.q10_microbial is not None, "q10_microbial is required when swoxygen is 2."
            assert self.specific_resp_humus is not None, "specific_resp_humus is required when swoxygen is 2."
            assert self.srl is not None, "srl is required when swoxygen is 2."
            assert self.swrootradius is not None, "swrootradius is required when swoxygen is 2."
            if self.swrootradius == 1:
                assert self.dry_mat_cont_roots is not None, "dry_mat_cont_roots is required when swrootradius is 1."
                assert self.air_filled_root_por is not None, "air_filled_root_por is required when swrootradius is 1."
                assert self.spec_weight_root_tissue is not None, "spec_weight_root_tissue is required when swrootradius is 1."
                assert self.var_a is not None, "var_a is required when swrootradius is 1."
            elif self.swrootradius == 2:
                assert self.root_radiuso2 is not None, "root_radiuso2 is required when swrootradius is 2."
        if self.swwrtnonox == 1:
            assert self.aeratecrit is not None, "aeratecrit is required when swwrtnonox is 1."

        return self


class DroughtStress(PySWAPBaseModel):
    """Drought stress settings for .crp file.

    Attributes:
        swdrought (Literal[1, 2]): Switch for drought stress

            * 1 - Drought stress according to Feddes et al. (1978)
            * 2 - rought stress according to De Jong van Lier et al. (2008)

        swjarvis (Optional[Literal[0, 1, 2, 3, 4]]): _DEPRECATED_ Switch for Jarvis model for water uptake reduction
        alphcrit: Optional[float] = _DEPRECATED_ Critical stress index (Jarvis, 1989) for compensation of root water uptake [0.2..1 -, R]
        hlim3h (Optional[float]): Pressure head below which water uptake reduction starts at high Tpot
        hlim3l (Optional[float]): Pressure head below which water uptake reduction starts at low Tpot
        hlim4 (Optional[float]): No water extraction at lower soil water pressure heads
        adcrh (Optional[float]): Level of high atmospheric demand, corresponding to HLIM3H
        adcrl (Optional[float]): Level of low atmospheric demand, corresponding to HLIM3L
        wiltpoint (Optional[float]): Minimum pressure head in leaves
        kstem (Optional[float]): Hydraulic conductance between leaf and root xylem
        rxylem (Optional[float]): Xylem radius
        rootradius (Optional[float]): Root radius
        kroot (Optional[float]): Radial hydraulic conductivity of root tissue
        rootcoefa (Optional[float]): Defines relative distance between roots at which mean soil water content occurs
        swhydrlift (Optional[Literal[0, 1]]): Switch for possibility hydraulic lift in root system
        rooteff (Optional[float]): Root system efficiency factor
        stephr (Optional[float]): Step between values of hroot and hxylem in iteration cycle
        criterhr (Optional[float]): Maximum difference of Hroot between iterations; convergence criterium
        taccur (Optional[float]): Maximum absolute difference between simulated and calculated potential transpiration rate
    """
    swdrought: Literal[1, 2]
    swjarvis: Optional[Literal[0, 1, 2, 3, 4]] = None
    alphcrit: Optional[float] = Field(default=None, ge=0.2, le=1.0)
    hlim3h: Optional[float] = Field(default=None, ge=-1.0e4, le=100.0)
    hlim3l: Optional[float] = Field(default=None, ge=-1.0e4, le=100.0)
    hlim4: Optional[float] = Field(default=None, ge=-1.6e4, le=100.0)
    adcrh: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    adcrl: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    wiltpoint: Optional[float] = Field(default=None, ge=-1.0e8, le=-1.0e2)
    kstem: Optional[float] = Field(default=None, ge=1.0e-10, le=10.0)
    rxylem: Optional[float] = Field(default=None, ge=1.0e-4, le=1.0)
    rootradius: Optional[float] = Field(default=None, ge=1.0e-4, le=1.0)
    kroot: Optional[float] = Field(default=None, ge=1.0e-10, le=1.0e10)
    rootcoefa: Optional[float] = Field(default=None, **UNITRANGE)
    swhydrlift: Optional[Literal[0, 1]] = None
    rooteff: Optional[float] = Field(default=None, **UNITRANGE)
    stephr: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    criterhr: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    taccur: Optional[float] = Field(default=None, ge=1.0e-5, le=1.0e-2)

    @model_validator(mode='after')
    def _validate_prepartion(self) -> Self:
        if self.swdrought == 1:
            assert self.hlim3h is not None, "hlim3h is required when swdrought is 1."
            assert self.hlim3l is not None, "hlim3l is required when swdrought is 1."
            assert self.hlim4 is not None, "hlim4 is required when swdrought is 1."
            assert self.adcrh is not None, "adcrh is required when swdrought is 1."
            assert self.adcrl is not None, "adcrl is required when swdrought is 1."
        if self.swdrought == 2:
            assert self.wiltpoint is not None, "wiltpoint is required when swdrought is 2."
            assert self.kstem is not None, "kstem is required when swdrought is 2."
            assert self.rxylem is not None, "rxylem is required when swdrought is 2."
            assert self.rootradius is not None, "rootradius is required when swdrought is 2."
            assert self.kroot is not None, "kroot is required when swdrought is 2."
            assert self.rootcoefa is not None, "rootcoefa is required when swdrought is 2."
            assert self.swhydrlift is not None, "swhydrlift is required when swdrought is 2."
            assert self.rooteff is not None, "rooteff is required when swdrought is 2."
            assert self.stephr is not None, "stephr is required when swdrought is 2."
            assert self.criterhr is not None, "criterhr is required when swdrought is 2."
            assert self.taccur is not None, "taccur is required when swdrought is 2."

        return self


class SaltStress(PySWAPBaseModel):
    """Salt stress settings for .crp file.

    Attributes:
        swsalinity (Literal[0, 1, 2]): Switch for salt stress

            * 0 - No salt stress
            * 1 - Maas and Hoffman reduction function
            * 2 - Use osmotic head

        saltmax (Optional[float]): Threshold salt concentration in soil water
        saltslope (Optional[float]): Decline of root water uptake above threshold
        salthead (Optional[float]): Conversion factor salt concentration (mg/cm3) into osmotic head (cm)
    """
    swsalinity: Literal[0, 1, 2]
    saltmax: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    saltslope: Optional[float] = Field(default=None, **UNITRANGE)
    salthead: Optional[float] = Field(default=None, ge=0.0, le=1000.0)

    @model_validator(mode='after')
    def _validate_prepartion(self) -> Self:
        if self.swsalinity == 1:
            assert self.saltmax is not None, "saltmax is required when swsalinity is 1."
            assert self.saltslope is not None, "saltslope is required when swsalinity is 1."
        elif self.swsalinity == 2:
            assert self.salthead is not None, "salthead is required when swsalinity is 2."

        return self


class CompensateRWUStress(PySWAPBaseModel):
    """Compensate root water uptake stress settings for .crp file.

    Attributes:
        swcompensate (Literal[0, 1, 2]): Switch for compensate root water uptake stress

            * 0 - No compensation
            * 1 - Compensation according to Jarvis (1989)
            * 2 - Compensation according to Walsum (2019)

        swstressor (Optional[Literal[1, 2, 3, 4, 5]]): Switch for stressor

            * 1 - Compensation of all stressors
            * 2 - Compensation of drought stress
            * 3 - Compensation of oxygen stress
            * 4 - Compensation of salinity stress
            * 5 - Compensation of frost stress

        alphacrit (Optional[float]): Critical stress index for compensation of root water uptake
        dcritrtz (Optional[float]): Threshold of rootzone thickness after which compensation occurs
    """
    swcompensate: Literal[0, 1, 2]
    swstressor: Optional[Literal[1, 2, 3, 4, 5]] = None
    alphacrit: Optional[float] = Field(default=None, ge=0.2, le=1.0)
    dcritrtz: Optional[float] = Field(default=None, ge=0.02, le=100.0)

    @model_validator(mode='after')
    def _validate_prepartion(self) -> Self:
        if self.swcompensate in [1, 2]:
            assert self.swstressor is not None, "swstressor is required when swcompensate is 1 or 2."
        if self.swcompensate == 1:
            assert self.alphacrit is not None, "alphacrit is required when swcompensate is 1."
        if self.swcompensate == 2:
            assert self.dcritrtz is not None, "dcritrtz is required when swcompensate is 2."

        return self


class Interception(PySWAPBaseModel):
    """Interception settings for .crp file.

    Attributes:
        swinter (Literal[0, 1, 2]): Switch for rainfall interception method

            * 0 - No interception
            * 1 - Agricultural crops (Von Hoyningen-Hune and Braden)
            * 2 - Trees and forests (Gash)

        cofab (Optional[float]): Interception coefficient, corresponding to maximum interception amount
        table_intertb (Optional[Table]): table with the following columns as a function of time T:

            * PFREE - Free throughfall coefficient
            * PSTEM - Stemflow coefficient
            * SCANOPY - Canopy storage coefficient
            * AVPREC = Average rainfall intensity
            * AVEVAP = Average evaporation intensity during rainfall from a wet canopy
    """
    swinter: Literal[0, 1, 2]
    cofab: Optional[float] = Field(default=None, **UNITRANGE)
    table_intertb: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_prepartion(self) -> Self:
        if self.swinter == 1:
            assert self.cofab is not None, "cofab is required when swinter is 1."
        elif self.swinter == 1:
            assert self.table_intertb is not None, "table_intertb is required when swinter is 2."

        return self


class CO2Correction(PySWAPBaseModel):
    """CO2 correction settings for WOFOST-type .crp file.

    Attributes:
        swco2 (Literal[0, 1]): Switch for assimilation correction due to CO2 impact

            * 0 - No CO2 assimilation correction
            * 1 - CO2 assimilation correction

        atmofil (Optional[str]): alternative filename for atmosphere.co2
        co2amaxtb (Optional[Arrays]): Correction of photosynthesis as a function of atmospheric CO2 concentration
        co2efftb (Optional[Arrays]): orrection of radiation use efficiency as a function of atmospheric CO2 concentration
        co2tratb (Optional[Arrays]): Correction of transpiration as a function of atmospheric CO2 concentration
    """

    swco2: Literal[0, 1]
    atmofil: Optional[str] = None
    co2amaxtb: Optional[Arrays] = None
    co2efftb: Optional[Arrays] = None
    co2tratb: Optional[Arrays] = None

    @model_validator(mode='after')
    def _validate_co2correction(self) -> Self:
        if self.swco2 == 1:
            assert self.atmofil is not None, 'amofil is required when swco2 is 1'
            assert self.co2amaxtb is not None, 'co2amaxtb is required when swco2 is 1'
            assert self.co2efftb is not None, 'co2efftb is required when swco2 is 1'
            assert self.co2tratb is not None, 'co2tratb is required when swco2 is 1'

        return self


class Preparation(PySWAPBaseModel):
    """Preparation, sowing and germination settings for .crp file.

    Attributes:
        swprep (Literal[0, 1]): Switch for preparation
        swsow (Literal[0, 1]): Switch for sowing
        swgerm (Literal[0, 1, 2]): Switch for germination

            * 0 - No germination
            * 1 - Germination with temperature sum
            * 2 - Germination with temperature sum and water potential

        swharv (Literal[0, 1]): Switch for harvest

            * 0 - Timing of harvest depends on end of growing period (CROPEND)
            * 1 - Timing of harvest depends on development stage (DVSEND)

        dvsend (Optional[float]): Development stage at harvest
        zprep (Optional[float]): Z-level for monitoring work-ability for the crop
        hprep (Optional[float]): Maximum pressure head during preparation
        maxprepdelay (Optional[int]): Maximum delay of preparation from start of growing season
        zsow (Optional[float]): Z-level for monitoring work-ability for the crop
        hsow (Optional[float]): Maximum pressure head during sowing
        ztempsow (Optional[float]): Z-level for monitoring temperature for sowing
        tempsow (Optional[float]): Soil temperature needed for sowing
        maxsowdelay (Optional[int]): Maximum delay of sowing from start of growing season
        tsumemeopt (Optional[float]): Temperature sum needed for crop emergence
        tbasem (Optional[float]): Minimum temperature, used for germination trajectory
        teffmx (Optional[float]): Maximum temperature, used for germination trajectory
        hdrygerm (Optional[float]): Pressure head rootzone for dry germination trajectory
        hwetgerm (Optional[float]): Pressure head rootzone for wet germination trajectory
        zgerm (Optional[float]): Z-level for monitoring average pressure head
        agerm (Optional[float]): A-coefficient Eq. 24/25 Feddes & Van Wijk
    """

    swprep: Literal[0, 1]
    swsow: Literal[0, 1]
    swgerm: Literal[0, 1, 2]
    swharv: Literal[0, 1]
    dvsend: Optional[float] = Field(default=None, ge=0.0, le=3.0)
    zprep: Optional[float] = Field(default=None, ge=-100.0, le=0.0)
    hprep: Optional[float] = Field(default=None, ge=-200.0, le=0.0)
    maxprepdelay: Optional[int] = Field(default=None, ge=1, le=366)
    zsow: Optional[float] = Field(default=None, ge=-100.0, le=0.0)
    hsow: Optional[float] = Field(default=None, ge=-200.0, le=0.0)
    ztempsow: Optional[float] = Field(default=None,  ge=-100.0, le=0.0)
    tempsow: Optional[float] = Field(default=None, ge=0.0, le=30.0)
    maxsowdelay: Optional[int] = Field(default=None, ge=1, le=366)
    tsumemeopt: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    tbasem: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    teffmx: Optional[float] = Field(default=None, ge=0.0, le=1000.0)
    hdrygerm: Optional[float] = Field(default=None, ge=-1000.0, le=1000.0)
    hwetgerm: Optional[float] = Field(default=None, ge=-100.0, le=1000.0)
    zgerm: Optional[float] = Field(default=None, ge=-100.0, le=1000.0)
    agerm: Optional[float] = Field(default=None, ge=0.0, le=1000.0)

    @model_validator(mode='after')
    def _validate_prepartion(self) -> Self:
        if self.swprep == 1:
            assert self.zprep is not None, "zprep is required when swprep is 1."
            assert self.hprep is not None, "hprep is required when swprep is 1."
            assert self.maxprepdelay is not None, "maxprepdelay is required when swprep is 1."

        if self.swsow == 1:
            assert self.zsow is not None, "zsow is required when swsow is 1."
            assert self.hsow is not None, "hsow is required when swsow is 1."
            assert self.ztempsow is not None, "ztempsow is required when swsow is 1."
            assert self.tempsow is not None, "tempsow is required when swsow is 1."
            assert self.maxsowdelay is not None, "maxsowdelay is required when swsow is 1."

        if self.swgerm in (1, 2):
            assert self.tsumemeopt is not None, "tsumemeopt is required when swgerm is 1 or 2."
            assert self.tbasem is not None, "tbasem is required when swgerm is 1 or 2."
            assert self.teffmx is not None, "teffmx is required when swgerm is 1 or 2."
        elif self.swgerm == 2:
            assert self.hdrygerm is not None, "hdrygerm is required when swgerm is 2."
            assert self.hwetgerm is not None, "hwetgerm is required when swgerm is 2."
            assert self.zgerm is not None, "zgerm is required when swgerm is 2."
            assert self.agerm is not None, "agerm is required when swgerm is 2."

        return self


class GrasslandManagement(PySWAPBaseModel):
    """Settings specific to the dynamic grass growth module.

    !!! warning

        Validation still required.

    Attributes:
        seqgrazmow (IntList): sequence of periods with different practices within calender year. Available options:

            * 1 - Grazing
            * 2 - Mowing
            * 3 - Grazing with dewooling

        swharvest (Literal[1, 2]): Switch for timing harvest, either for mowing or grazing

            * 1 - Use dry matter threshold
            * 2 - Use fixed dates

        dateharvest Optional[(DateList)]: harvest dates (maximum 999)
        swdmgrz Optional[(Literal[1, 2])]: Switch for dry matter threshold to trigger harvest by grazing

            * 1 - Use fixed threshold
            * 2 - Use flexible threshold

        dmgrazing Optional[(Arrays)]: Minimum dry matter amount for cattle to enter the field [0..1d6 kg DM/ha, R]
        dmgrztb Optional[(int)]: List threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger grazing as function of daynumber [1..366 d, R]
        maxdaygrz Optional[(int)]: Maximum growing period after harvest [1..366 -, I]
        swlossgrz Optional[(Literal[0, 1])]: Switch for losses due to insufficient pressure head during grazing

            * 0 - No loss
            * 1 - Losses due to treading

        tagprest Optional[(float)]: Minimum amount of above ground DM after grazing [0..1d6 kg DM/ha, R]
        dewrest Optional[(float)]: Remaining yield above ground after dewooling event [0..1d6 kg DM/ha, R]
        table_lsda (Optional[Table]): Actual livestock density of each grazing period
        table_lsdb (Optional[Table]): Relation between livestock density, number of grazing days and dry matter uptake
        swdmmow Optional[(int)]: Switch for dry matter threshold to trigger harvest by mowing

            * 1 - Use fixed threshold
            * 2 - Use flexible threshold

        dmharvest Optional[(float)]: Threshold of above ground dry matter to trigger mowing [0..1d6 kg DM/ha, R]
        daylastharvest Optional[(int)]: Last calendar day on which mowing may occur [1..366 -, I]
        dmlastharvest Optional[(float)]: Minimum above ground dry matter for mowing on last date [0..1d6 kg DM/ha, R]
        dmmowtb Optional[(int)]: Dry matter mowing threshold
        maxdaymow Optional[(int)]:Maximum growing period after harvest [1..366 -, I]
        swlossmow Optional[(int)]: Switch for losses due to insufficient pressure head during mowing

            * 0 - No loss
            * 1 - Losses due to treading

        mowrest Optional[(float)]: Remaining yield above ground after mowing event [0..1d6 kg DM/ha, R]
        table_dmmowdelay Optional[(Optional[Table])]: Relation between dry matter harvest [0..1d6 kg/ha, R] and days of delay in regrowth [0..366 d, I] after mowing
        swpotrelmf (int): Switch for calculation of potential yield

            * 1 - theoretical potential yield
            * 2 - attainable yield

        relmf (float): Relative management factor to reduce theoretical potential yield to attainable yield [0..1 -, R]
    """

    seqgrazmow: IntList
    swharvest: Literal[1, 2]
    dateharvest: Optional[DateList] = None
    swdmgrz: Optional[Literal[1, 2]] = None
    dmgrazing: Optional[Arrays] = None
    dmgrztb: Optional[Arrays] = None
    maxdaygrz: Optional[int] = None
    swlossgrz: Optional[Literal[0, 1]] = None
    tagprest: Optional[float] = None
    dewrest: Optional[float] = None
    table_lsda: Optional[Table] = None
    table_lsdb: Optional[Table] = None
    swdmmow: Optional[int] = None
    dmharvest: Optional[float] = None
    daylastharvest: Optional[int] = None
    dmlastharvest: Optional[float] = None
    dmmowtb: Optional[Arrays] = None
    maxdaymow: Optional[int] = None
    swlossmow: Optional[int] = None
    mowrest: Optional[float] = None
    table_dmmowdelay: Optional[Table] = None
    swpotrelmf: int
    relmf: float

    # @model_validator(mode='after')
    # def _validate_grassland_management(self) -> Self:
    #     if self.swharvest == 2:
    #         assert self.dateharvest is not None, "dateharvest is required when swharvest is 2."
    #     if self.swdmgrz == 1:
    #         assert self.dmgrazing is not None, "dmgrazing is required when swdmgrz is 1."
    #         assert self.dmgrztb is not None, "dmgrztb is required when swdmgrz is 1."
    #         assert self.maxdaygrz is not None, "maxdaygrz is required when swdmgrz is 1."
    #     if self.swdmgrz == 2:
    #         assert self.tagprest is not None, "tagprest is required when swdmgrz is 2."
    #         assert self.dewrest is not None, "dewrest is required when swdmgrz is 2."
    #         assert self.table_lsda is not None, "table_lsda


class CropFile(PySWAPBaseModel):
    """Main class for the .crp file.

    This class collects all the settings for the crop file. Currently the types of the 
    attributes are set to Any because the validation is not yet implemented.

    Attributes:
        name (str): Name of the crop
        path (Optional[str]): Path to the .crp file
        prep (Optional[Preparation]): Preparation settings
        cropdev_settings (Optional[CropDevelopmentSettings | 
            CropDevelopmentSettingsFixed | 
            CropDevelopmentSettingsWOFOST]): Crop development settings
        oxygenstress (Optional[OxygenStress]): Oxygen stress settings
        droughtstress (Optional[DroughtStress]): Drought stress settings
        saltstress (Optional[SaltStress]): Salt stress settings
        compensaterwu (Optional[CompensateRWUStress]): Compensate root water uptake stress settings
        interception (Optional[Interception]): Interception settings
        scheduledirrigation (Optional[ScheduledIrrigation]): Scheduled irrigation settings
        grassland_management (Optional[GrasslandManagement]): Grassland management settings
    """

    name: str = Field(exclude=True)
    path: Optional[str] = None
    prep: Optional[Preparation] = None
    cropdev_settings: Optional[CropDevelopmentSettings |
                               CropDevelopmentSettingsFixed |
                               CropDevelopmentSettingsWOFOST |
                               CropDevelopmentSettingsGrass] = None
    oxygenstress: Optional[OxygenStress] = None
    droughtstress: Optional[DroughtStress] = None
    saltstress: Optional[SaltStress] = SaltStress(swsalinity=0)
    compensaterwu: Optional[CompensateRWUStress] = CompensateRWUStress(
        swcompensate=0)
    interception: Optional[Interception] = None
    scheduledirrigation: Optional[ScheduledIrrigation] = ScheduledIrrigation(
        schedule=0)
    grasslandmanagement: Optional[GrasslandManagement] = None
    co2correction: Optional[CO2Correction] = None

    @computed_field(return_type=str)
    def content(self):
        if self.path:
            return open_file(self.path)
        else:
            return self._concat_sections()
