"""
## Crop module

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
    This script will undergo major changes in the future. Some things to
    improve include smoother integration with WOFOST configuration files
    (yaml) and code readability."""


from typing import Literal

from pydantic import Field, computed_field
import pandera as pa
from pandera.typing import Series

from pyswap.core.io.ascii import open_ascii, save_ascii
from pyswap.core.fields import Arrays, DateList, IntList, Table
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.mixins import SerializableMixin, YAMLValidatorMixin, FileMixin
from pyswap.core.fields import Table
from pyswap.core.valueranges import DVSRANGE, UNITRANGE, YEARRANGE
from pyswap.core.basemodel import BaseTableModel
from pyswap.components.irrigation import ScheduledIrrigation

__all__ = [
    "CropDevelopmentSettings", "CropDevelopmentSettingsWOFOST", "CropDevelopmentSettingsFixed", "OxygenStress", 
    "CropDevelopmentSettingsGrass", "DroughtStress", "SaltStress", "CompensateRWUStress", "Interception", "CO2Correction", "Preparation",
    "CropFile", "Crop",
]


class CropDevelopmentSettings(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    table_dvs_cf: Table | None = None
    table_dvs_ch: Table | None = None
    albedo: float | None = Field(default=None, **UNITRANGE)
    rsc: float | None = Field(default=None, ge=0.0, le=1.0e6)
    rsw: float | None = Field(default=None, ge=0.0, le=1.0e6)
    # In WOFOST reference yaml files this is called TSUM1
    tsumea: float = Field(default=None, ge=0.0, le=1.0e4)
    # In WOFOST reference yaml files this is called TSUM2
    tsumam: float = Field(default=None, ge=0.0, le=1.0e4)
    # In SWAP this parameter seems to meen something different than in the
    # WOFOST template. The range of value is the same though.
    tbase: float | None = Field(default=None, ge=-10.0, le=30.0)
    kdif: float = Field(ge=0.0, le=2.0)
    kdir: float = Field(ge=0.0, le=2.0)
    swrd: Literal[1, 2, 3] | None = None
    rdtb: Arrays | None = None
    rdi: float = Field(default=None, ge=0.0, le=1000.0)
    rri: float = Field(default=None, ge=0.0, le=100.0)
    rdc: float = Field(default=None, ge=0.0, le=1000.0)
    swdmi2rd: Literal[0, 1] | None = None
    rlwtb: Arrays | None = None
    wrtmax: float = Field(default=None, ge=0.0, le=1.0e5)
    swrdc: Literal[0, 1] = 0
    rdctb: Arrays


class CropDevelopmentSettingsWOFOST(CropDevelopmentSettings):
    """Additional settings as defined for the WOFOST model.

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

    idsl: Literal[0, 1, 2] | None = None  # for grass at least
    dtsmtb: Arrays | None = None  # for grass at least
    dlo: float | None = Field(default=None, ge=0.0, le=24.0)
    dlc: float | None = Field(default=None, ge=0.0, le=24.0)
    vernsat: float | None = Field(default=None, ge=0.0, le=100.0)
    vernbase: float | None = Field(default=None, ge=0.0, le=100.0)
    verndvs: float | None = Field(default=None, ge=0.0, le=0.3)
    verntb: Arrays | None = None
    tdwi: float = Field(ge=0.0, le=10_000)
    laiem: float = Field(ge=0.0, le=10)
    rgrlai: float = Field(**UNITRANGE)
    spa: float | None = Field(**UNITRANGE, default=None)
    ssa: float = Field(**UNITRANGE)
    span: float = Field(**YEARRANGE)
    slatb: Arrays
    eff: float = Field(ge=0.0, le=10.0)
    amaxtb: Arrays
    tmpftb: Arrays
    tmnftb: Arrays
    cvo: float | None = Field(**UNITRANGE, default=None)  # for grass at least
    cvl: float = Field(**UNITRANGE)
    cvr: float = Field(**UNITRANGE)
    cvs: float = Field(**UNITRANGE)
    q10: float = Field(ge=0.0, le=5.0)
    rml: float = Field(**UNITRANGE)
    rmo: float | None = Field(**UNITRANGE, default=None)  # for grass at least
    rmr: float = Field(**UNITRANGE)
    rms: float = Field(**UNITRANGE)
    rfsetb: Arrays
    frtb: Arrays
    fltb: Arrays
    fstb: Arrays
    fotb: Arrays | None = None  # for grass at least
    perdl: float = Field(ge=0.0, le=3.0)
    rdrrtb: Arrays
    rdrstb: Arrays


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
    lcc: int | None = Field(default=None, **YEARRANGE)
    swgc: Literal[1, 2]
    gctb: Arrays
    kytb: Arrays | None = None


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
    tsumtemp: float | None = None
    tsumdepth: float | None = None
    tsumtime: float | None = None


class OxygenStress(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    >> move it to the Model class validation at the end, when all the params are available
    """

    swoxygen: Literal[0, 1, 2]
    swwrtnonox: Literal[0, 1]
    swoxygentype: Literal[1, 2] | None = None
    aeratecrit: float | None = Field(default=None, ge=0.0001, le=1.0)
    hlim1: float | None = Field(default=None, ge=-100.0, le=100.0)
    hlim2u: float | None = Field(default=None, ge=-1000.0, le=100.0)
    hlim2l: float | None = Field(default=None, ge=-1000.0, le=100.0)
    q10_microbial: float | None = Field(default=None, ge=1.0, le=4.0)
    specific_resp_humus: float | None = Field(default=None, **UNITRANGE)
    srl: float | None = Field(default=None, ge=0.0, le=1.0e10)
    swrootradius: Literal[1, 2] | None = None
    dry_mat_cont_roots: float | None = Field(default=None, **UNITRANGE)
    air_filled_root_por: float | None = Field(default=None, **UNITRANGE)
    spec_weight_root_tissue: float | None = Field(default=None, ge=0.0, le=1.0e5)
    var_a: float | None = Field(default=None, **UNITRANGE)
    root_radiuso2: float | None = Field(default=None, ge=1.0e-6, le=0.1)
    q10_root: float | None = Field(default=None, ge=1.0, le=4.0)
    f_senes: float | None = Field(default=None, **UNITRANGE)
    c_mroot: float | None = Field(default=None, **UNITRANGE)
    mrftb: Arrays | None = None
    wrtb: Arrays | None = None


class DroughtStress(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    swjarvis: Literal[0, 1, 2, 3, 4] | None = None
    alphcrit: float | None = Field(default=None, ge=0.2, le=1.0)
    hlim3h: float | None = Field(default=None, ge=-1.0e4, le=100.0)
    hlim3l: float | None = Field(default=None, ge=-1.0e4, le=100.0)
    hlim4: float | None = Field(default=None, ge=-1.6e4, le=100.0)
    adcrh: float | None = Field(default=None, ge=0.0, le=5.0)
    adcrl: float | None = Field(default=None, ge=0.0, le=5.0)
    wiltpoint: float | None = Field(default=None, ge=-1.0e8, le=-1.0e2)
    kstem: float | None = Field(default=None, ge=1.0e-10, le=10.0)
    rxylem: float | None = Field(default=None, ge=1.0e-4, le=1.0)
    rootradius: float | None = Field(default=None, ge=1.0e-4, le=1.0)
    kroot: float | None = Field(default=None, ge=1.0e-10, le=1.0e10)
    rootcoefa: float | None = Field(default=None, **UNITRANGE)
    swhydrlift: Literal[0, 1] | None = None
    rooteff: float | None = Field(default=None, **UNITRANGE)
    stephr: float | None = Field(default=None, ge=0.0, le=10.0)
    criterhr: float | None = Field(default=None, ge=0.0, le=10.0)
    taccur: float | None = Field(default=None, ge=1.0e-5, le=1.0e-2)


class SaltStress(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    saltmax: float | None = Field(default=None, ge=0.0, le=100.0)
    saltslope: float | None = Field(default=None, **UNITRANGE)
    salthead: float | None = Field(default=None, ge=0.0, le=1000.0)


class CompensateRWUStress(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    swstressor: Literal[1, 2, 3, 4, 5] | None = None
    alphacrit: float | None = Field(default=None, ge=0.2, le=1.0)
    dcritrtz: float | None = Field(default=None, ge=0.02, le=100.0)


class Interception(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    cofab: float | None = Field(default=None, **UNITRANGE)
    table_intertb: Table | None = None


class CO2Correction(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    atmofil: str | None = None
    co2amaxtb: Arrays | None = None
    co2efftb: Arrays | None = None
    co2tratb: Arrays | None = None


class Preparation(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    dvsend: float | None = Field(default=None, ge=0.0, le=3.0)
    zprep: float | None = Field(default=None, ge=-100.0, le=0.0)
    hprep: float | None = Field(default=None, ge=-200.0, le=0.0)
    maxprepdelay: int | None = Field(default=None, ge=1, le=366)
    zsow: float | None = Field(default=None, ge=-100.0, le=0.0)
    hsow: float | None = Field(default=None, ge=-200.0, le=0.0)
    ztempsow: float | None = Field(default=None, ge=-100.0, le=0.0)
    tempsow: float | None = Field(default=None, ge=0.0, le=30.0)
    maxsowdelay: int | None = Field(default=None, ge=1, le=366)
    tsumemeopt: float | None = Field(default=None, ge=0.0, le=1000.0)
    tbasem: float | None = Field(default=None, ge=0.0, le=1000.0)
    teffmx: float | None = Field(default=None, ge=0.0, le=1000.0)
    hdrygerm: float | None = Field(default=None, ge=-1000.0, le=1000.0)
    hwetgerm: float | None = Field(default=None, ge=-100.0, le=1000.0)
    zgerm: float | None = Field(default=None, ge=-100.0, le=1000.0)
    agerm: float | None = Field(default=None, ge=0.0, le=1000.0)


class GrasslandManagement(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
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
    dateharvest: DateList | None = None
    swdmgrz: Literal[1, 2] | None = None
    dmgrazing: Arrays | None = None
    dmgrztb: Arrays | None = None
    maxdaygrz: int | None = None
    swlossgrz: Literal[0, 1] | None = None
    tagprest: float | None = None
    dewrest: float | None = None
    table_lsda: Table | None = None
    table_lsdb: Table | None = None
    swdmmow: int | None = None
    dmharvest: float | None = None
    daylastharvest: int | None = None
    dmlastharvest: float | None = None
    dmmowtb: Arrays | None = None
    maxdaymow: int | None = None
    swlossmow: int | None = None
    mowrest: float | None = None
    table_dmmowdelay: Table | None = None
    swpotrelmf: int
    relmf: float


class CropFile(PySWAPBaseModel, FileMixin, SerializableMixin):
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

    >> This is a good place to implement a separate model validator, if there are dependencies between the sections.
    """

    name: str = Field(exclude=True)
    path: str | None = None
    prep: Subsection | None = None
    cropdev_settings: Subsection | None = None
    oxygenstress: Subsection | None = None
    droughtstress: Subsection | None = None
    saltstress: Subsection | None = SaltStress(swsalinity=0)
    compensaterwu: Subsection | None = CompensateRWUStress(swcompensate=0)
    interception: Subsection | None = None
    scheduledirrigation: Subsection | None = ScheduledIrrigation(schedule=0)
    grasslandmanagement: Subsection | None = None
    co2correction: Subsection | None = None

    @property
    def crp(self) -> str:
        """Return the model string of the .crp file."""
        return self.model_string()


class Crop(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Holds the crop settings of the simulation.

    Attributes:
        swcrop (int): Switch for crop:

            * 0 - Bare soil.
            * 1 - Simulate crop.

        rds (Optional[float]): Rooting depth of the crop [cm].
        table_croprotation (Optional[Table]): Table with crop rotation data.
        cropfiles (Optional[List[CropFile]]): List of crop files.

    Methods:
        write_crop: Write the crop files.
    """

    swcrop: Literal[0, 1]
    rds: float | None = Field(default=None, ge=1, le=5000)
    table_croprotation: Table | None = None
    cropfiles: dict[str, CropFile] | None = Field(default=None, exclude=True)

    def write_crop(self, path: str):
        count = 0
        for name, cropfile in self.cropfiles.items():
            count += 1
            save_ascii(string=cropfile.crp, extension="crp", fname=name, path=path)

        print(f"{count} crop file(s) saved.")


#------------------------------------------ Crop tables ------------------------------------------#
__all__.extend([
    "RDTB", "RDCTB", "GCTB", "CHTB", "KYTB", "MRFTB", "WRTB",
    "CROPROTATION", "DTSMTB", "SLATB", "AMAXTB", "TMPFTB", "TMNFTB", "RFSETB", "FRTB", "FLTB",
    "FSTB", "FOTB", "RDRRTB", "RDRSTB", "DMGRZTB", "LSDATB", "LSDBTB", "RLWTB", "DMMOWTB", "DMMOWDELAY",
    "CHTB_GRASS", "SLATB_GRASS", "AMAXTB_GRASS", "RFSETB_GRASS", "FRTB_GRASS", "FLTB_GRASS", "FSTB_GRASS", 
    "RDRRTB_GRASS", "RDRSTB_GRASS"
])

class RDTB(BaseTableModel):
    """Rooting Depth [0..1000 cm, R], as a function of development stage [0..2 -, R].

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RD (Series[float]): Rooting depth of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RD: Series[float] = pa.Field(ge=0.0, le=100.0)


class RDCTB(BaseTableModel):
    """List root density [0..100 cm/cm3, R] as function of relative rooting depth [0..1 -, R]

    Attributes:
        RRD (Series[float]): Relative rooting depth of the crop.
        RDENS (Series[float]): Root density of the crop.

    """

    RRD: Series[float] = pa.Field(ge=0.0, le=100.0)
    RDENS: Series[float] = pa.Field(**UNITRANGE)


class GCTB(BaseTableModel):
    """Leaf Area Index [0..12 (m2 leaf)/(m2 soil), R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        LAI (Series[float]): Leaf Area Index of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    LAI: Series[float] = pa.Field(ge=0.0, le=12.0)


class CHTB(BaseTableModel):
    """Crop Height [0..1.d4 cm, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        CH (Series[float]): Crop height of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    CH: Series[float] = pa.Field(ge=0.0, le=1.0e4)


class KYTB(BaseTableModel):
    """Yield response factor [0..5 -, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        KY (Series[float]): Yield response factor of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    KY: Series[float] = pa.Field(ge=0.0, le=5.0)


class MRFTB(BaseTableModel):
    """Ratio root total respiration / maintenance respiration [1..5.0 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        MAX_RESP_FACTOR (Series[float]): Ratio root total respiration / maintenance respiration.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    MAX_RESP_FACTOR: Series[float] = pa.Field(ge=1.0, le=5.0)


class WRTB(BaseTableModel):
    """dry weight of roots at soil surface [0..10 kg/m3, R], as a function of development stage [0..2 -,R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        W_ROOT_SS (Series[float]): Dry weight of roots at soil surface.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    W_ROOT_SS: Series[float] = pa.Field(ge=0.0, le=10.0)


class CROPROTATION(BaseTableModel):
    """Crop rotation settings

    Attributes:
        CROPSTART (Series[pa.DateTime]): Start date of the crop.
        CROPEND (Series[pa.DateTime]): End date of the crop.
        CROPFIL (Series[str]): Crop file name.
        CROPTYPE (Series[int]): Crop module type

            * 1 - simple
            * 2 - detailed, WOFOST general
            * 3 - detailed, WOFOST grass
    """

    CROPSTART: Series[pa.DateTime]  # type: ignore
    CROPEND: Series[pa.DateTime]  # type: ignore
    CROPFIL: Series[str]
    CROPTYPE: Series[int] = pa.Field(ge=1, le=3)


# WOFOST-specific tables
class DTSMTB(BaseTableModel):
    """increase in temperature sum [0..60 oC, R] as function of daily average temperature [0..100 oC, R]

    Attributes:
        TAV (Series[float]): Daily average temperature.
        DTSM (Series[float]): Increase in temperature sum.
    """

    TAV: Series[float] = pa.Field(ge=0.0, le=100.0)
    DTSM: Series[float] = pa.Field(ge=0.0, le=60.0)


class SLATB(BaseTableModel):
    """leaf area [0..1 ha/kg, R] as function of crop development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        SLA (Series[float]): Leaf area.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB(BaseTableModel):
    """maximum CO2 assimilation rate [0..100 kg/ha/hr, R] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        AMAX (Series[float]): Maximum CO2 assimilation rate.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    AMAX: Series[float] = pa.Field(ge=0.0, le=100.0)


class TMPFTB(BaseTableModel):
    """reduction factor of AMAX [-, R] as function of average day temperature [-10..50 oC, R]

    Attributes:
        TAVD (Series[float]): Minimum temperature.
        TMPF (Series[float]): Reduction factor of AMAX.
    """

    TAVD: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMPF: Series[float] = pa.Field(ge=0.0, le=1.0)


class TMNFTB(BaseTableModel):
    """reduction factor of AMAX [-, R] as function of minimum day temperature [-10..50 oC, R]

    Attributes:
        TMNR (Series[float]): Minimum temperature.
        TMNF (Series[float]): Reduction factor of AMAX.
    """

    TMNR: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMNF: Series[float] = pa.Field(ge=0.0, le=1.0)


class RFSETB(BaseTableModel):
    """reduction factor of senescence [-, R] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RFSE (Series[float]): Reduction factor of senescence.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RFSE: Series[float] = pa.Field(ge=0.0, le=1.0)


class FRTB(BaseTableModel):
    """fraction of total dry matter increase partitioned to the roots [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FR: Series[float] = pa.Field(ge=0.0, le=1.0)


class FLTB(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the leaves [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FL: Series[float] = pa.Field(ge=0.0, le=1.0)


class FSTB(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the stems [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FS: Series[float] = pa.Field(ge=0.0, le=1.0)


class FOTB(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the storage organs [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FO (Series[float]): Fraction of total above ground dry matter increase partitioned to the storage organs.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FO: Series[float] = pa.Field(ge=0.0, le=1.0)


class RDRRTB(BaseTableModel):
    """relative death rates of roots [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RDRR (Series[float]): Relative death rates of roots.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB(BaseTableModel):
    """relative death rates of stems [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RDRS (Series[float]): Relative death rates of stems.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RDRS: Series[float] = pa.Field(ge=0.0)


class DMGRZTB(BaseTableModel):
    """threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger grazing as function of daynumber [1..366 d, R]

    Attributes:
        DNR (Series[float]): Day number.
        DMGRZ (Series[float]): Dry matter growth rate of roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMGRZ: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class LSDATB(BaseTableModel):
    """Actual livestock density of each grazing period

    !!! note

        total number of periods should be equal to number of periods in SEQGRAZMOW

    Attributes:
        SEQNR (Series[int]): number of the sequence period with mowing/grazing [0..366 d, I]
        LSDA (Series[float]): Actual Live Stock Density of the grazing period [0.0..1000.0 LS/ha, R]
    """

    SEQNR: Series[int] = pa.Field(**YEARRANGE)
    LSDA: Series[float] = pa.Field(ge=0.0, le=1000.0)


class LSDBTB(BaseTableModel):
    """Relation between livestock density, number of grazing days and dry matter uptake

    Attributes:
        LSDB (Series[float]): Basic Live Stock Density [0.0..1000.0 LS/ha, R]
        DAYSGRAZING (Series[float]): Maximum days of grazing [0.0..366.0 d, R]
        UPTGRAZING (Series[float]): Dry matter uptake by grazing [0.0..1000.0 kg/ha, R] (kg/ha DM)
        LOSSGRAZING (Series[float]): Dry matter loss during grazing due to droppings and treading [0.0..1000.0 kg/ha, R] (kg/ha DM)
    """

    LSDB: Series[float] = pa.Field(ge=0.0, le=1000.0)
    DAYSGRAZING: Series[float] = pa.Field(**YEARRANGE)
    UPTGRAZING: Series[float] = pa.Field(ge=0.0, le=1000.0)
    LOSSGRAZING: Series[float] = pa.Field(ge=0.0, le=1000.0)


class RLWTB(BaseTableModel):
    """rooting depth RL [0..5000 cm, R] as function of root weight RW [0..5000 kg DM/ha, R]

    Attributes:
        RW (Series[float]): rooting depth
        RL (Series[float]): root weight
    """

    RW: Series[float] = pa.Field(ge=0.0, le=5000.0)
    RL: Series[float] = pa.Field(ge=0.0, le=5000.0)


class DMMOWTB(BaseTableModel):
    """List threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger mowing as function of daynumber [1..366 d, R]

    !!! note

        maximum 20 records


    Attributes:
        DNR (Series[float]): Day number.
        DMMOW (Series[float]): threshold of above ground dry matter [0..1d6 kg DM/ha, R]
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMMOW: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class DMMOWDELAY(BaseTableModel):
    """Relation between dry matter harvest [0..1d6 kg/ha, R] and days of delay in regrowth [0..366 d, I] after mowing

    Attributes:
        DMMOWDELAY (Series[float]): Dry matter harvest [0..1d6 kg/ha, R]
        DAYDELAY (Series[int]): days of delay in regrowth [0..366 d, I]
    """

    DMMOWDELAY: Series[float] = pa.Field(ge=0.0, le=1.0e6)
    DAYDELAY: Series[int] = pa.Field(**YEARRANGE)


class CHTB_GRASS(BaseTableModel):
    """Crop Height [0..1.d4 cm, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): day number.
        CH (Series[float]): Crop height of the crop.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    CH: Series[float] = pa.Field(ge=0.0, le=1.0e4)


class SLATB_GRASS(BaseTableModel):
    """leaf area [0..1 ha/kg, R] as function of crop development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        SLA (Series[float]): Leaf area.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB_GRASS(BaseTableModel):
    """maximum CO2 assimilation rate [0..100 kg/ha/hr, R] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        AMAX (Series[float]): Maximum CO2 assimilation rate.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    AMAX: Series[float] = pa.Field(ge=0.0, le=100.0)


class RFSETB_GRASS(BaseTableModel):
    """reduction factor of senescence [-, R] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RFSE (Series[float]): Reduction factor of senescence.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RFSE: Series[float] = pa.Field(**UNITRANGE)


class FRTB_GRASS(BaseTableModel):
    """fraction of total dry matter increase partitioned to the roots [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FR: Series[float] = pa.Field(**UNITRANGE)


class FLTB_GRASS(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the leaves [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FL: Series[float] = pa.Field(**UNITRANGE)


class FSTB_GRASS(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the stems [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FS: Series[float] = pa.Field(**UNITRANGE)


class RDRRTB_GRASS(BaseTableModel):
    """relative death rates of roots [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RDRR (Series[float]): Relative death rates of roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB_GRASS(BaseTableModel):
    """relative death rates of stems [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RDRS (Series[float]): Relative death rates of stems.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RDRS: Series[float] = pa.Field(ge=0.0)
