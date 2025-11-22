# mypy: disable-error-code="call-overload, misc, type-arg"
# The type-arg here causes problems with passing the actual type to the alias
# Subsection. This however helps to type hinting, so it has to stay that way.
"""Crop settings and crop files for SWAP model.

Similar to the .dra or .swp files, the .crp file is a configuration file for the SWAP model.
The classes in this module represent distincs sections of the .crp file. The main class is the
`CropFile` class which holds the settings for the crop simulation.

SWAP has three modes for crop simulations which users define in the CROPROTATION _table in the .swp file:

    * 1 - simple crop settings - use CropDevelopmentSettingsFixed
    * 2 - detailed, WOFOST general settings - use CropDevelopmentSettingsWOFOST
    * 3 - dynamic grass growth model - use CropDevelopmentSettingsGrass

For each choice, the .crp file will look different. Therefore, multiple classes
 are defined in this module to deal with those different settings.

Classes:
    CropFile: Class for the .crp file.
    CropDevelopmentSettingsWOFOST: Class for the crop development settings in WOFOST.
    CropDevelopmentSettingsFixed: Class for the fixed crop development settings.
    CropDevelopmentSettingsGrass: Class for the grass crop development settings.
    OxygenStress: Class for the oxygen stress settings.
    DroughtStress: Class for the drought stress settings.
    SaltStress: Class for the salt stress settings.
    CompensateRWUStress: Class for the compensate root water uptake stress settings.
    Interception: Class for the interception settings.
    CO2Correction: Class for the CO2 correction settings.
    ScheduledIrrigation: Class for the scheduled irrigation settings.
    Preparation: Class for the preparation settings.
"""

from typing import (
    Any,
    Literal as _Literal,
)

from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.irrigation import ScheduledIrrigation as _ScheduledIrrigation
from pyswap.components.tables import (
    AMAXTB,
    CFTB,
    CHTB,
    CROPROTATION,
    DMGRZTB,
    DMMOWDELAY,
    DMMOWTB,
    DTSMTB,
    FLTB,
    FOTB,
    FRTB,
    FSTB,
    GCTB,
    KYTB,
    LSDA,
    LSDATB,
    LSDBTB,
    MRFTB,
    RDCTB,
    RDRRTB,
    RDRSTB,
    RDTB,
    RFSETB,
    RLWTB,
    SLATB,
    TMNFTB,
    TMPFTB,
    VERNRTB,
    WRTB,
)
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Arrays as _Arrays,
    Decimal2f as _Decimal2f,
    IntList as _IntList,
    Subsection as _Subsection,
    Table as _Table,
)
from pyswap.core.valueranges import (
    UNITRANGE as _UNITRANGE,
    YEARRANGE as _YEARRANGE,
)
from pyswap.db.cropdb import CropVariety as _CropVariety
from pyswap.utils.mixins import (
    FileMixin as _FileMixin,
    SerializableMixin as _SerializableMixin,
    YAMLUpdateMixin as _YAMLUpdateMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "AMAXTB",
    "CFTB",
    "CHTB",
    "CROPROTATION",
    "DMGRZTB",
    "DMMOWDELAY",
    "DMMOWTB",
    "DTSMTB",
    "FLTB",
    "FOTB",
    "FRTB",
    "FSTB",
    "GCTB",
    "KYTB",
    "LSDA",
    "LSDATB",
    "LSDBTB",
    "MRFTB",
    "RDCTB",
    "RDRRTB",
    "RDRSTB",
    "RDTB",
    "RFSETB",
    "RLWTB",
    "SLATB",
    "TMNFTB",
    "TMPFTB",
    "VERNRTB",
    "WRTB",
    "CO2Correction",
    "CompensateRWUStress",
    "Crop",
    "CropDevelopmentSettingsFixed",
    "CropDevelopmentSettingsGrass",
    "CropDevelopmentSettingsWOFOST",
    "CropFile",
    "DroughtStress",
    "Interception",
    "OxygenStress",
    "Preparation",
    "SaltStress",
    "_CropDevelopmentSettings",
]


class _CropDevelopmentSettings(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _YAMLUpdateMixin
):
    """Crop development settings.

    !!! note:

        CropDevelopmentSettings is a base class for the different crop
        development settings (type 1, 2 and 3). Crop parameters can be read from
        WOFOST database. Because some names of the same parameters are different
        between the wofost and swap templates, the alias parameter is used to
        rename the parameters in serialization to SWAP compatible .crp file.
        Currently it applies to TSUM1 and TSUM2.

    Attributes:
        wofost_variety (CropVariety): Crop variety settings.
        swcf (Literal[1, 2]): Choose between crop factor and crop height for simulation of
            * 1 - Crop factor, when using ETref from meteo or Penman-Monteith.
            * 2 - Crop height, when using Penman-Monteith with actual crop height, albedo and canopy resistance.
        cftb (Optional[_Table]): Table with crop factors [0..2 -] as a function of development stage.
        chtb (Optional[_Table]): Table with crop height [0..1e4 cm] as a function of development stage.
        albedo (Optional[float]): Crop reflection coefficient [0..1.0 -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6 s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6 s/m].
        tsumea (float): Temperature sum from emergence to anthesis [0..1e4 degrees C].
        tsumam (float): Temperature sum from anthesis to maturity [1..1e4 degrees C].
        tbase (Optional[float]): Start value of temperature sum [-10..30 degrees C].
        kdif (float): Extinction coefficient for diffuse visible light [0..2 -].
        kdir (float): Extinction coefficient for direct visible light [0..2 -].
        swrd (Optional[Literal[1, 2, 3]]): Switch development of root growth.
            * 1 - Root growth depends on development stage.
            * 2 - Root growth depends on maximum daily increase.
            * 3 - Root growth depends on available root biomass.
        rdtb (Optional [_Arrays]): Rooting depth [0..1000 cm] as a function of development stage [0..2 -].
        rdi (float): Initial rooting depth [0..1000 cm].
        rri (float): Maximum daily increase in rooting depth [0..100 cm].
        rdc (float): Maximum rooting depth of particular crop [0..1000 cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.
            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.
        rlwtb (Optional _Arrays]): rooting depth [0..5000 cm] as function of root weight [0..5000 kg DM/ha].
        wrtmax (float): Maximum root weight [0..1e5 kg DM/ha].
        swrdc (Literal[0, 1]): Switch for calculation of relative root density.
            * 0 - Root density is not modified.
            * 1 - Root density is modified based on root water extraction.
        TODO: add parameters related to swdrc=1: fgwrt, fdwrt, wrtmin
        rdctb (_Arrays): root density [0..1 -] as function of relative rooting depth [0..1 -].
    """

    # add in model config that additional attributes are allowed
    # model_config = _ConfigDict(
    #     extra="allow"
    # )

    wofost_variety: Any | None = _Field(default=None, exclude=True)

    swcf: _Literal[1, 2] | None = None
    cftb: _Table | None = None
    chtb: _Table | None = None
    albedo: _Decimal2f | None = _Field(default=None, **_UNITRANGE)
    rsc: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e6)
    rsw: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e6)
    tsum1: _Decimal2f | None = _Field(alias="tsumea", default=None, ge=0.0, le=1.0e4)
    tsum2: _Decimal2f | None = _Field(alias="tsumam", default=None, ge=0.0, le=1.0e4)
    tbase: _Decimal2f | None = _Field(default=None, ge=-10.0, le=30.0)
    kdif: _Decimal2f | None = _Field(default=None, ge=0.0, le=2.0)
    kdir: _Decimal2f | None = _Field(default=None, ge=0.0, le=2.0)
    swrd: _Literal[1, 2, 3] | None = None
    rdtb: _Arrays | None = None
    rdi: _Decimal2f | None = _Field(default=None, ge=0.0, le=1000.0)
    rri: _Decimal2f | None = _Field(default=None, ge=0.0, le=100.0)
    rdc: _Decimal2f | None = _Field(default=None, ge=0.0, le=1000.0)
    swdmi2rd: _Literal[0, 1] | None = None
    rlwtb: _Arrays | None = None
    wrtmax: _Decimal2f | None = _Field(default=None, ge=0.0, le=1.0e5)
    swrdc: _Literal[0, 1] | None = None
    rdctb: _Arrays | None = None


class CropDevelopmentSettingsWOFOST(_CropDevelopmentSettings):
    """Additional settings as defined for the WOFOST model.

    Attributes:
        wofost_variety (CropVariety): Crop variety settings.
        swcf (Literal[1, 2]): Choose between crop factor and crop height for simulation of
            * 1 - Crop factor, when using ETref from meteo or Penman-Monteith.
            * 2 - Crop height, when using Penman-Monteith with actual crop height, albedo and canopy resistance.
        cftb (Optional[_Table]): Table with crop factors [0..2 -] as a function of development stage.
        chtb (Optional[_Table]): Table with crop height [0..1e4 cm] as a function of development stage.
        albedo (Optional[float]): Crop reflection coefficient [0..1.0 -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6 s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6 s/m].
        tsumea (float): Temperature sum from emergence to anthesis [0..1e4 degrees C].
        tsumam (float): Temperature sum from anthesis to maturity [1..1e4 degrees C].
        tbase (Optional[float]): Start value of temperature sum [-10..30 degrees C].
        kdif (float): Extinction coefficient for diffuse visible light [0..2 -].
        kdir (float): Extinction coefficient for direct visible light [0..2 -].
        swrd (Optional[Literal[1, 2, 3]]): Switch development of root growth.
            * 1 - Root growth depends on development stage.
            * 2 - Root growth depends on maximum daily increase.
            * 3 - Root growth depends on available root biomass.
        rdtb (Optional [_Arrays]): Rooting depth [0..1000 cm] as a function of development stage [0..2 -].
        rdi (float): Initial rooting depth [0..1000 cm].
        rri (float): Maximum daily increase in rooting depth [0..100 cm].
        rdc (float): Maximum rooting depth of particular crop [0..1000 cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.
            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.
        rlwtb (Optional _Arrays]): rooting depth [0..5000 cm] as function of root weight [0..5000 kg DM/ha].
        wrtmax (float): Maximum root weight [0..1e5 kg DM/ha].
        swrdc (Literal[0, 1]): Switch for calculation of relative root density.
            * 0 - Root density is not modified.
            * 1 - Root density is modified based on root water extraction.
        TODO: add parameters related to swdrc=1: fgwrt, fdwrt, wrtmin
        rdctb (_Arrays): root density [0..1 -] as function of relative rooting depth [0..1 -].
        idsl (Literal[0, 1, 2]): Switch for crop development.
            * 0 - Depends on temperature
            * 1 - Depends on temperature and daylength
            * 2 - Depends on temperature, daylength and vernalisation factor
        dtsmtb (_Arrays): List increase in temperature sum [0..60 degrees C] as function of daily average temperature.
        dlo (Optional[float]): Optimum day length for crop development [0..24 hr].
        dlc (Optional[float]): Minimum day length [0..24 hr].
        vernsat (Optional[float]): Saturated vernalisation requirement.
        vernbase (Optional[float]): Base vernalisation requirement.
        verndvs (Optional[float]): Critical development stage after which the effect of vernalisation is halted.
        vernrtb (Optional [_Arrays]): _Table with rate of vernalisation as function of average air temperature. In WOFOST it's called this way. Aliased
            to verntb for SWAP.
        tdwi (float): Initial total crop dry weight [0..10000 kg/ha].
        laiem (float): Leaf area index at emergence [0..10 m2/m2].
        rgrlai (float): Maximum relative increase in LAI [0..1 m2/m2/d].
        spa (float): Specific pod area [0..1 ha/kg].
        ssa (float): Specific stem area [0..1 ha/kg].
        span (float): Life span under leaves under optimum conditions [0..366 d].
        slatb (_Arrays): List specific leaf area [0..1 ha/kg] as function of crop development stage.
        eff (float): Light use efficiency for real leaf [0..10 kg/ha/hr/(J m2 s)].
        amaxtb (_Arrays): List maximum CO2 assimilation rate [0..100 kg/ha/hr] as function of development stage.
        tmpftb (_Arrays): List reduction factor of AMAX [-] as function of average day temperature.
        tmnftb (_Arrays): List reduction factor of AMAX [-] as function of minimum day temperature.
        cvo (float): Efficiency of conversion into storage organs [0..1 kg/kg].
        cvl (float): Efficiency of conversion into leaves [0..1 kg/kg].
        cvr (float): Efficiency of conversion into roots [0..1 kg/kg].
        cvs (float): Efficiency of conversion into stems [0..1 kg/kg].
        q10 (float): Increase in respiration rate with temperature [0..5 /10 degrees C].
        rml (float): Maintenance respiration rate of leaves [0..1 kgCH2O/kg/d].
        rmo (float): Maintenance respiration rate of storage organs [0..1 kgCH2O/kg/d].
        rmr (float): Maintenance respiration rate of roots [0..1 kgCH2O/kg/d].
        rms (float): Maintenance respiration rate of stems [0..1 kgCH2O/kg/d].
        rfsetb (_Arrays): List reduction factor of senescence [0..2 -] as function of development stage.
        frtb (_Arrays): List fraction of total dry matter increase partitioned to the roots [0..1 kg/kg] as function of development stage.
        fltb (_Arrays): List fraction of total above ground dry matter increase partitioned to the leaves [0..1 kg/kg] as function of development stage.
        fstb (_Arrays): List fraction of total above ground dry matter increase partitioned to the stems [0..1 kg/kg] as function of development stage.
        fotb (_Arrays): List fraction of total above ground dry matter increase partitioned to the storage organs [0..1 kg/kg] as function of development stage.
        perdl (float): Maximum relative death rate of leaves due to water stress [0..3 /d].
        rdrrtb (_Arrays): List relative death rates of roots [0..1 kg/kg/d] as function of development stage.
        rdrstb (_Arrays): List relative death rates of stems [0..1 kg/kg/d] as function of development stage.
    """

    idsl: _Literal[0, 1, 2] | None = None
    dtsmtb: _Arrays | None = None
    dlo: float | None = _Field(default=None, ge=0.0, le=24.0)
    dlc: float | None = _Field(default=None, ge=0.0, le=24.0)
    vernsat: float | None = _Field(default=None, ge=0.0, le=100.0)
    vernbase: float | None = _Field(default=None, ge=0.0, le=100.0)
    verndvs: float | None = _Field(default=None, ge=0.0, le=0.3)
    vernrtb: _Arrays | None = _Field(default=None, alias="verntb")
    tdwi: float | None = _Field(default=None, ge=0.0, le=10_000)
    laiem: float | None = _Field(default=None, ge=0.0, le=10)
    rgrlai: float | None = _Field(default=None, **_UNITRANGE)
    spa: float | None = _Field(**_UNITRANGE, default=None)
    ssa: float | None = _Field(default=None, **_UNITRANGE)
    span: float | None = _Field(default=None, **_YEARRANGE)
    slatb: _Arrays | None = None
    eff: float | None = _Field(default=None, ge=0.0, le=10.0)
    amaxtb: _Arrays | None = None
    tmpftb: _Arrays | None = None
    tmnftb: _Arrays | None = None
    cvo: float | None = _Field(default=None, **_UNITRANGE)
    cvl: float | None = _Field(default=None, **_UNITRANGE)
    cvr: float | None = _Field(default=None, **_UNITRANGE)
    cvs: float | None = _Field(default=None, **_UNITRANGE)
    q10: float | None = _Field(default=None, ge=0.0, le=5.0)
    rml: float | None = _Field(default=None, **_UNITRANGE)
    rmo: float | None | None = _Field(**_UNITRANGE, default=None)
    rmr: float | None = _Field(default=None, **_UNITRANGE)
    rms: float | None = _Field(default=None, **_UNITRANGE)
    rfsetb: _Arrays | None = None
    frtb: _Arrays | None = None
    fltb: _Arrays | None = None
    fstb: _Arrays | None = None
    fotb: _Arrays | None = None
    perdl: float | None = _Field(default=None, ge=0.0, le=3.0)
    rdrrtb: _Arrays | None = None
    rdrstb: _Arrays | None = None


class CropDevelopmentSettingsFixed(_CropDevelopmentSettings):
    """Fixed crop development settings (Additionaly to CropDevelopmentSettings).

    Attributes:
        swcf (Literal[1, 2]): Choose between crop factor and crop height for simulation of
            * 1 - Crop factor, when using ETref from meteo or Penman-Monteith.
            * 2 - Crop height, when using Penman-Monteith with actual crop height, albedo and canopy resistance.
        cftb (Optional[_Table]): Table with crop factors [0..2 -] as a function of development stage.
        chtb (Optional[_Table]): Table with crop height [0..1e4 cm] as a function of development stage.
        albedo (Optional[float]): Crop reflection coefficient [0..1.0 -].
        rsc (Optional[float]): Minimum canopy resistance [0..1e6 s/m].
        rsw (Optional[float]): Canopy resistance of intercepted water [0..1e6 s/m].
        tsumea (float): Temperature sum from emergence to anthesis [0..1e4 degrees C].
        tsumam (float): Temperature sum from anthesis to maturity [1..1e4 degrees C].
        tbase (Optional[float]): Start value of temperature sum [-10..30 degrees C].
        kdif (float): Extinction coefficient for diffuse visible light [0..2 -].
        kdir (float): Extinction coefficient for direct visible light [0..2 -].
        swrd (Optional[Literal[1, 2, 3]]): Switch development of root growth.
            * 1 - Root growth depends on development stage.
            * 2 - Root growth depends on maximum daily increase.
            * 3 - Root growth depends on available root biomass.
        rdtb (Optional [_Arrays]): Rooting depth [0..1000 cm] as a function of development stage [0..2 -].
        rdi (float): Initial rooting depth [0..1000 cm].
        rri (float): Maximum daily increase in rooting depth [0..100 cm].
        rdc (float): Maximum rooting depth of particular crop [0..1000 cm].
        swdmi2rd (Optional[Literal[0, 1]]): Switch for calculation rooting depth.
            * 0 - Rooting depth increase is related to availability assimilates for roots.
            * 1 - Rooting depth increase is related to relative dry matter increase.
        rlwtb (Optional _Arrays]): rooting depth [0..5000 cm] as function of root weight [0..5000 kg DM/ha].
        wrtmax (float): Maximum root weight [0..1e5 kg DM/ha].
        swrdc (Literal[0, 1]): Switch for calculation of relative root density.
            * 0 - Root density is not modified.
            * 1 - Root density is modified based on root water extraction.
        TODO: add parameters related to swdrc=1: fgwrt, fdwrt, wrtmin
        rdctb (_Arrays): root density [0..1 -] as function of relative rooting depth [0..1 -].
        idev (Literal[1, 2]): Duration of crop growing period

            * 1 - Duration is fixed
            * 2 - Duration is variable

        lcc (Optional[int]): Duration of the crop growing period
        swgc (Literal[1, 2]): Choose between Leaf Area Index or Soil Cover Fraction

            * 1 - LAI
            * 2 - SCF

        gctb  _Arrays): Soil Cover Fraction as a function of development stage
    """

    idev: _Literal[1, 2] | None = None
    lcc: int | None = _Field(default=None, **_YEARRANGE)
    swgc: _Literal[1, 2] | None = None
    gctb: _Arrays | None = None
    kytb: _Arrays | None = None


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

    swtsum: _Literal[0, 1, 2] | None = None
    tsumtemp: float | None = None
    tsumdepth: float | None = None
    tsumtime: float | None = None


class OxygenStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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
        _table_max_resp_factor (Optional[_Table]): Ratio root total respiration / maintenance respiration as a function of development stage
        _table_dvs_w_root_ss (Optional[_Table]): List dry weight of roots at soil surface as a function of development stage

    TODO: Find a way to validate the parameters that are required when the
    croptype=1 and swoxygen=2 (currently I cannot access the croptype parameter)
    >> move it to the Model class validation at the end, when all the params are available
    """

    swoxygen: _Literal[0, 1, 2] | None = None
    swwrtnonox: _Literal[0, 1] | None = None
    swoxygentype: _Literal[1, 2] | None = None
    aeratecrit: float | None = _Field(default=None, ge=0.0001, le=1.0)
    hlim1: float | None = _Field(default=None, ge=-100.0, le=100.0)
    hlim2u: float | None = _Field(default=None, ge=-1000.0, le=100.0)
    hlim2l: float | None = _Field(default=None, ge=-1000.0, le=100.0)
    q10_microbial: float | None = _Field(default=None, ge=1.0, le=4.0)
    specific_resp_humus: float | None = _Field(default=None, **_UNITRANGE)
    srl: float | None = _Field(default=None, ge=0.0, le=1.0e10)
    swrootradius: _Literal[1, 2] | None = None
    dry_mat_cont_roots: float | None = _Field(default=None, **_UNITRANGE)
    air_filled_root_por: float | None = _Field(default=None, **_UNITRANGE)
    spec_weight_root_tissue: float | None = _Field(default=None, ge=0.0, le=1.0e5)
    var_a: float | None = _Field(default=None, **_UNITRANGE)
    root_radiuso2: float | None = _Field(default=None, ge=1.0e-6, le=0.1)
    q10_root: float | None = _Field(default=None, ge=1.0, le=4.0)
    f_senes: float | None = _Field(default=None, **_UNITRANGE)
    c_mroot: float | None = _Field(default=None, **_UNITRANGE)
    mrftb: _Arrays | None = None
    wrtb: _Arrays | None = None


class DroughtStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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

    swdrought: _Literal[1, 2] | None = None
    swjarvis: _Literal[0, 1, 2, 3, 4] | None = None
    alphcrit: float | None = _Field(default=None, ge=0.2, le=1.0)
    hlim3h: float | None = _Field(default=None, ge=-1.0e4, le=100.0)
    hlim3l: float | None = _Field(default=None, ge=-1.0e4, le=100.0)
    hlim4: float | None = _Field(default=None, ge=-1.6e4, le=100.0)
    adcrh: float | None = _Field(default=None, ge=0.0, le=5.0)
    adcrl: float | None = _Field(default=None, ge=0.0, le=5.0)
    wiltpoint: float | None = _Field(default=None, ge=-1.0e8, le=-1.0e2)
    kstem: float | None = _Field(default=None, ge=1.0e-10, le=10.0)
    rxylem: float | None = _Field(default=None, ge=1.0e-4, le=1.0)
    rootradius: float | None = _Field(default=None, ge=1.0e-4, le=1.0)
    kroot: float | None = _Field(default=None, ge=1.0e-10, le=1.0e10)
    rootcoefa: float | None = _Field(default=None, **_UNITRANGE)
    swhydrlift: _Literal[0, 1] | None = None
    rooteff: float | None = _Field(default=None, **_UNITRANGE)
    stephr: float | None = _Field(default=None, ge=0.0, le=10.0)
    criterhr: float | None = _Field(default=None, ge=0.0, le=10.0)
    taccur: float | None = _Field(default=None, ge=1.0e-5, le=1.0e-2)


class SaltStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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

    swsalinity: _Literal[0, 1, 2] | None = None
    saltmax: float | None = _Field(default=None, ge=0.0, le=100.0)
    saltslope: float | None = _Field(default=None, **_UNITRANGE)
    salthead: float | None = _Field(default=None, ge=0.0, le=1000.0)


class CompensateRWUStress(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
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

    swcompensate: _Literal[0, 1, 2] | None = None
    swstressor: _Literal[1, 2, 3, 4, 5] | None = None
    alphacrit: float | None = _Field(default=None, ge=0.2, le=1.0)
    dcritrtz: float | None = _Field(default=None, ge=0.02, le=100.0)


class Interception(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Interception settings for .crp file.

    Attributes:
        swinter (Literal[0, 1, 2]): Switch for rainfall interception method

            * 0 - No interception
            * 1 - Agricultural crops (Von Hoyningen-Hune and Braden)
            * 2 - Trees and forests (Gash)

        cofab (Optional[float]): Interception coefficient, corresponding to maximum interception amount
        _table_intertb (Optional[_Table]): _table with the following columns as a function of time T:

            * PFREE - Free throughfall coefficient
            * PSTEM - Stemflow coefficient
            * SCANOPY - Canopy storage coefficient
            * AVPREC = Average rainfall intensity
            * AVEVAP = Average evaporation intensity during rainfall from a wet canopy
    """

    swinter: _Literal[0, 1, 2] | None = None
    cofab: float | None = _Field(default=None, **_UNITRANGE)
    intertb: _Table | None = None


class CO2Correction(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _YAMLUpdateMixin
):
    """CO2 correction settings for WOFOST-type .crp file.

    Attributes:
        swco2 (Literal[0, 1]): Switch for assimilation correction due to CO2 impact

            * 0 - No CO2 assimilation correction
            * 1 - CO2 assimilation correction

        atmofil (Optional[str]): alternative filename for atmosphere.co2
        co2amaxtb (Optional [_Arrays]): Correction of photosynthesis as a function of atmospheric CO2 concentration
        co2efftb (Optional [_Arrays]): orrection of radiation use efficiency as a function of atmospheric CO2 concentration
        co2tratb (Optional [_Arrays]): Correction of transpiration as a function of atmospheric CO2 concentration
    """

    _validation: bool = _PrivateAttr(default=False)
    wofost_variety: _CropVariety | None = _Field(default=None, exclude=True)

    swco2: _Literal[0, 1] | None = None
    atmofil: str | None = None
    co2amaxtb: _Arrays | None = None
    co2efftb: _Arrays | None = None
    co2tratb: _Arrays | None = None


class Preparation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Preparation, sowing and germination settings for .crp file.

    Attributes:
        swprep (Literal[0, 1]): Switch for preparation.
            * 1 - No preparation.
            * 2 - Preparation before start of crop growth.
        zprep (Optional[float]): Z-level for monitoring work-ability for the crop [-100..0 cm].
        hprep (Optional[float]): Maximum pressure head during preparation [-200..0 cm].
        maxprepdelay (Optional[int]): Maximum delay of preparation from start of growing season [1..366 d].
        swsow (Literal[0, 1]): Switch for sowing
            * 0 - No sowing
            * 1 - Sowing before start of crop growth
        zsow (Optional[float]): Z-level for monitoring work-ability for the crop [-100..0 cm].
        hsow (Optional[float]): Maximum pressure head during sowing [-200..0 cm].
        ztempsow (Optional[float]): Z-level for monitoring temperature for sowing [-100..0 cm].
        tempsow (Optional[float]): Soil temperature needed for sowing [0..30 degrees C].
        maxsowdelay (Optional[int]): Maximum delay of sowing from start of growing season [1..366 d].
        swgerm (Literal[0, 1, 2]): Switch for germination.
            * 0 - No germination.
            * 1 - Germination with temperature sum.
            * 2 - Germination with temperature sum and water potential.
        tsumemeopt (Optional[float]): Temperature sum needed for crop emergence [0..1000 degrees C]
        tbasem (Optional[float]): Minimum temperature, used for germination trajectory [0..40 degrees C].
        teffmx (Optional[float]): Maximum temperature, used for germination trajectory [0..40 degrees C].
        hdrygerm (Optional[float]): Pressure head rootzone for dry germination trajectory [-1000..-0.01 cm].
        hwetgerm (Optional[float]): Pressure head rootzone for wet germination trajectory [-1000..-0.01 cm].
        zgerm (Optional[float]): Z-level for monitoring average pressure head for germination [-100..0 cm].
        agerm (Optional[float]): A-coefficient Eq. 24/25 Feddes & Van Wijk (1988) [0..1000 -].
        swharv (Literal[0, 1]): Switch for harvest.
            * 0 - Timing of harvest depends on end of growing period (CROPEND).
            * 1 - Timing of harvest depends on development stage (DVSEND).
        dvsend (Optional[float]): Development stage at harvest [0..3 -].
    """

    swprep: _Literal[0, 1] | None = _Field(default=None)
    swsow: _Literal[0, 1] | None = None
    swgerm: _Literal[0, 1, 2] | None = None
    swharv: _Literal[0, 1] | None = None
    dvsend: float | None = _Field(default=None, ge=0.0, le=3.0)
    zprep: float | None = _Field(default=None, ge=-100.0, le=0.0)
    hprep: float | None = _Field(default=None, ge=-200.0, le=0.0)
    maxprepdelay: int | None = _Field(default=None, ge=1, le=366)
    zsow: float | None = _Field(default=None, ge=-100.0, le=0.0)
    hsow: float | None = _Field(default=None, ge=-200.0, le=0.0)
    ztempsow: float | None = _Field(default=None, ge=-100.0, le=0.0)
    tempsow: float | None = _Field(default=None, ge=0.0, le=30.0)
    maxsowdelay: int | None = _Field(default=None, ge=1, le=366)
    tsumemeopt: float | None = _Field(default=None, ge=0.0, le=1000.0)
    tbasem: float | None = _Field(default=None, ge=0.0, le=1000.0)
    teffmx: float | None = _Field(default=None, ge=0.0, le=1000.0)
    hdrygerm: float | None = _Field(default=None, ge=-1000.0, le=1000.0)
    hwetgerm: float | None = _Field(default=None, ge=-100.0, le=1000.0)
    zgerm: float | None = _Field(default=None, ge=-100.0, le=1000.0)
    agerm: float | None = _Field(default=None, ge=0.0, le=1000.0)


class GrasslandManagement(
    _PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin, _YAMLUpdateMixin
):
    """Settings specific to the dynamic grass growth module.

    Attributes:
        seqgrazmow (_IntList): sequence of periods with different practices within calender year. Available options:

            * 1 - Grazing
            * 2 - Mowing
            * 3 - Grazing with dewooling

        swharvest (Literal[1, 2]): Switch for timing harvest, either for mowing or grazing

            * 1 - Use dry matter threshold
            * 2 - Use fixed dates

        dateharvest Optional[(_DateList)]: harvest dates (maximum 999)
        swdmgrz Optional[(Literal[1, 2])]: Switch for dry matter threshold to trigger harvest by grazing

            * 1 - Use fixed threshold
            * 2 - Use flexible threshold

        dmgrazing Optional[ _Arrays)]: Minimum dry matter amount for cattle to enter the field [0..1d6 kg DM/ha, R]
        dmgrztb Optional[(int)]: List threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger grazing as function of daynumber [1..366 d, R]
        maxdaygrz Optional[(int)]: Maximum growing period after harvest [1..366 -, I]
        swlossgrz Optional[(Literal[0, 1])]: Switch for losses due to insufficient pressure head during grazing

            * 0 - No loss
            * 1 - Losses due to treading

        tagprest Optional[(float)]: Minimum amount of above ground DM after grazing [0..1d6 kg DM/ha, R]
        dewrest Optional[(float)]: Remaining yield above ground after dewooling event [0..1d6 kg DM/ha, R]
        _table_lsda (Optional[_Table]): Actual livestock density of each grazing period
        _table_lsdb (Optional[_Table]): Relation between livestock density, number of grazing days and dry matter uptake
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
        _table_dmmowdelay Optional[(Optional[_Table])]: Relation between dry matter harvest [0..1d6 kg/ha, R] and days of delay in regrowth [0..366 d, I] after mowing
        swpotrelmf (int): Switch for calculation of potential yield

            * 1 - theoretical potential yield
            * 2 - attainable yield

        relmf (float): Relative management factor to reduce theoretical potential yield to attainable yield [0..1 -, R]
    """

    seqgrazmow: _IntList | None = None
    swharvest: _Literal[1, 2] | None = None
    dateharvest: _Arrays | None = None
    swdmgrz: _Literal[1, 2] | None = None
    dmgrazing: _Decimal2f | None = None
    dmgrztb: _Arrays | None = None
    maxdaygrz: int | None = None
    swlossgrz: _Literal[0, 1] | None = None
    tagprest: _Decimal2f | None = None
    dewrest: _Decimal2f | None = None
    lsda: _Table | None = None
    lsdb: _Table | None = None
    swdmmow: int | None = None
    dmharvest: _Decimal2f | None = None
    daylastharvest: int | None = None
    dmlastharvest: _Decimal2f | None = None
    dmmowtb: _Arrays | None = None
    maxdaymow: int | None = None
    swlossmow: int | None = None
    mowrest: _Decimal2f | None = None
    dmmowdelay: _Table | None = None
    swpotrelmf: int | None = None
    relmf: _Decimal2f | None = None


class CropFile(_PySWAPBaseModel, _FileMixin, _SerializableMixin):
    """Main class for the .crp file.

    This class collects all the settings for the crop file. Currently the types of the
    attributes are set to Any because the validation is not yet implemented.

    Attributes:
        name (str): Name of the crop
        path (Optional[str]): Path to the .crp file
        prep (Optional[Preparation]): Preparation settings
        cropdev_settings (Optional[CropDevelopmentSettings]): Crop development settings
        oxygenstress (Optional[OxygenStress]): Oxygen stress settings
        droughtstress (Optional[DroughtStress]): Drought stress settings
        saltstress (Optional[SaltStress]): Salt stress settings
        compensaterwu (Optional[CompensateRWUStress]): Compensate root water uptake stress settings
        interception (Optional[Interception]): Interception settings
        scheduledirrigation (Optional[ScheduledIrrigation]): Scheduled irrigation settings
        grassland_management (Optional[GrasslandManagement]): Grassland management settings
    """

    _extension: bool = _PrivateAttr(default="crp")

    name: str = _Field(exclude=True)
    path: str | None = None
    prep: _Subsection[Preparation] | None = None
    cropdev_settings: (
        _Subsection[
            CropDevelopmentSettingsFixed
            | CropDevelopmentSettingsWOFOST
            | CropDevelopmentSettingsGrass
        ]
        | None
    ) = None
    oxygenstress: _Subsection[OxygenStress] | None = None
    droughtstress: _Subsection[DroughtStress] | None = None
    saltstress: _Subsection[SaltStress] | None = SaltStress(swsalinity=0)
    compensaterwu: _Subsection[CompensateRWUStress] | None = CompensateRWUStress(
        swcompensate=0
    )
    interception: _Subsection[Interception] | None = None
    scheduledirrigation: _Subsection[_ScheduledIrrigation] | None = (
        _ScheduledIrrigation(schedule=0)
    )
    grasslandmanagement: _Subsection[GrasslandManagement] | None = None
    co2correction: _Subsection[CO2Correction] | None = None

    @property
    def crp(self) -> str:
        """Return the model string of the .crp file.

        The addition validates all the crop files in the dictionary.
        """
        for comp in CropFile.model_fields:
            item = getattr(self, comp)
            if hasattr(item, "validate_with_yaml"):
                item._validation = True
                item.validate_with_yaml()
        return self.model_string()


class Crop(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Crop settings of the simulation.

    Attributes:
        swcrop (int): Switch for crop:

            * 0 - Bare soil.
            * 1 - Simulate crop.

        rds (Optional[float]): Rooting depth of the crop [cm].
        croprotation (Optional[_Table]): _Table with crop rotation data.
        cropfiles (Optional[List[CropFile]]): List of crop files.

    Methods:
        write_crop: Write the crop files.
    """

    swcrop: _Literal[0, 1, None] = None
    rds: float | None = _Field(default=None, ge=1, le=5000)
    croprotation: _Table | None = None
    cropfiles: dict[str, CropFile] = _Field(default_factory=dict, exclude=True)

    def write_crop(self, path: str):
        for name, cropfile in self.cropfiles.items():
            cropfile.save_file(string=cropfile.crp, fname=name, path=path)
