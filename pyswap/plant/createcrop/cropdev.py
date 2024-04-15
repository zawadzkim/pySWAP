"""Script for part 1: crop development
TODO: implement predefined types, for example: Switch = Literal[0, 1]; DayOfYear = Field(ge=1, le=366)
TODO: implement ranges
"""
from ...core.utils.basemodel import PySWAPBaseModel
from ...core.utils.fields import Table, Arrays
from ...core.utils.valueranges import UNITRANGE, YEARRANGE
from typing import Literal, Optional
from pydantic import Field, model_validator


class CropDevelopmentSettings(PySWAPBaseModel):
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
    swrd: Literal[1, 2, 3]
    rdtb: Optional[Arrays] = None
    rdi: float = Field(default=None, ge=0.0, le=1000.0)
    rri: float = Field(default=None, ge=0.0, le=100.0)
    rdc: float = Field(default=None, ge=0.0, le=1000.0)
    swdmi2rd: Optional[Literal[0, 1]] = None
    rlwtb: Optional[Arrays] = None
    wrtmax: float = Field(default=None, ge=0.0, le=1.0e5)
    swrdc: Literal[0, 1] = 0
    rdctb: Arrays

    # @model_validator(mode='after')
    # def _validate_crop_base(self):
    #     if self.swcf == 1:
    #         assert self.table_dvs_cf is not None, "table_dvs_cf is required when swcf is 1."
    #     elif self.swcf == 2:
    #         assert self.table_dvs_ch is not None, "table_dvs_ch is required when swcf is 2."
    #         assert self.albedo is not None, "albedo is required when swcf is 2."
    #         assert self.rsc is not None, "rsc is required when swcf is 2."
    #         assert self.rsw is not None, "rsw is required when swcf is 2."
    #     if self.swrd == 1:
    #         assert self.rdtb is not None, "rdtb is required when swrd is 1."
    #     elif self.swrd == 2:
    #         assert self.rdi is not None, "rdi is required when swrd is 2."
    #         assert self.rri is not None, "rri is required when swrd is 2."
    #         assert self.rdc is not None, "rdc is required when swrd is 2."
    #         assert self.swdmi2rd is not None, "swdmi2rd is required when swrd is 2."
    #     elif self.swrd == 3:
    #         assert self.rlwtb is not None, "rlwtb is required when swrd is 3."
    #         assert self.wrtmax is not None, "wrtmax is required when swrd is 3."


class CropDevelopmentSettingsWOFOST(CropDevelopmentSettings):
    """Use serialization_alias to change the parameter names who are different between WOFOST and SWAP."""
    idsl: Literal[0, 1, 2]
    dtsmtb: Arrays
    dlo: Optional[float] = Field(default=None, ge=0.0, le=24.0)
    dlc: Optional[float] = Field(default=None, ge=0.0, le=24.0)
    vernsat: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    vernbase: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    verndvs: Optional[float] = Field(default=None, ge=0.0, le=0.3)
    verntb: Optional[Arrays] = None
    tdwi: float = Field(ge=0.0, le=10_000)
    laiem: float = Field(ge=0.0, le=10)
    rgrlai: float = Field(**UNITRANGE)
    spa: float = Field(**UNITRANGE)
    ssa: float = Field(**UNITRANGE)
    span: float = Field(**YEARRANGE)
    slatb: Arrays
    eff:  float = Field(ge=0.0, le=10.0)
    amaxtb: Arrays
    tmpftb: Arrays
    tmnftb: Arrays
    cvo: float = Field(**UNITRANGE)
    cvl: float = Field(**UNITRANGE)
    cvr: float = Field(**UNITRANGE)
    cvs: float = Field(**UNITRANGE)
    q10: float = Field(ge=0.0, le=5.0)
    rml: float = Field(**UNITRANGE)
    rmo: float = Field(**UNITRANGE)
    rmr: float = Field(**UNITRANGE)
    rms: float = Field(**UNITRANGE)
    rfsetb: Arrays
    frtb: Arrays
    fltb: Arrays
    fstb: Arrays
    fotb: Arrays
    perdl: float = Field(ge=0.0, le=3.0)
    rdrrtb: Arrays
    rdrstb: Arrays

    # @model_validator(mode='before')
    # def _validate_crop_wofost(self):
    #     if self.idsl in [0, 1]:
    #         assert self.dlc is not None, "dlc is required when idsl is either 1 or 2."
    #         assert self.dlo is not None, "dlo is required when idsl is either 1 or 2."
    #     elif self.idsl == 2:
    #         assert self.vernsat is not None, "vernsat is required when idsl is 2."
    #         assert self.vernbase is not None, "vernbase is required when idsl is 2."
    #         assert self.verndvs is not None, "verndvs is required when idsl is 2."
    #         assert self.verntb is not None, "verntb is required when idsl is 2."


class CropDevelopmentSettingsFixed(CropDevelopmentSettings):
    """Crop development settings (parts 1-xx form the template)

    I noticed an issue with the tables here. They are actually arrays (each
    array is a column) that are preceeded by the variable name and "=". That variable
    name is the same for all options of tables which have different column names (e.g., DVS/LAI or
    DVS/SCF) but the variable name is the same (e.g., GCTB).
    TODO: implement a check of the column before the df is converted to string.
    """
    idev: Literal[1, 2]
    lcc: Optional[int] = Field(default=None, **YEARRANGE)
    swgc: Literal[1, 2]
    gctb: Arrays

    # @model_validator(mode='after')
    # def _validate_crop_fixed(self):
    #     if self.idev == 1:
    #         assert self.lcc is not None, "lcc is required when idev is 1."
    #     elif self.idev == 2:
    #         assert self.tsumea is not None, "tsumea is required when idev is 2."
    #         assert self.tsumam is not None, "tsumam is required when idev is 2."
    #         assert self.tbase is not None, "tbase is required when idev is 2."


class OxygenStress(PySWAPBaseModel):
    """TODO: Find a way to validate the parameters that are required when the
    croptype=1 and swoxygen=2 (currently I cannot access the croptype parameter)
    """
    swoxygen: Literal[0, 1, 2]
    swwrtnonox: Literal[0, 1]
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
    table_max_resp_factor: Optional[Table] = None
    table_dvs_w_root_ss: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_prepartion(self):
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


class DroughtStress(PySWAPBaseModel):
    swdrought: Literal[1, 2]
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
    def _validate_prepartion(self):
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


class SaltStress(PySWAPBaseModel):
    swsalinity: Literal[0, 1, 2]
    saltmax: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    saltslope: Optional[float] = Field(default=None, **UNITRANGE)
    salthead: Optional[float] = Field(default=None, ge=0.0, le=1000.0)

    @model_validator(mode='after')
    def _validate_prepartion(self):
        if self.swsalinity == 1:
            assert self.saltmax is not None, "saltmax is required when swsalinity is 1."
            assert self.saltslope is not None, "saltslope is required when swsalinity is 1."
        elif self.swsalinity == 2:
            assert self.salthead is not None, "salthead is required when swsalinity is 2."


class CompensateRWUStress(PySWAPBaseModel):
    swcompensate: Literal[0, 1, 2]
    swstressor: Optional[Literal[0, 1, 2, 3, 4, 5]] = None
    alphacrit: Optional[float] = Field(default=None, ge=0.2, le=1.0)
    dcritrtz: Optional[float] = Field(default=None, ge=0.02, le=100.0)

    @model_validator(mode='after')
    def _validate_prepartion(self):
        if self.swcompensate in [1, 2]:
            assert self.swstressor is not None, "swstressor is required when swcompensate is 1 or 2."
        if self.swcompensate == 1:
            assert self.alphacrit is not None, "alphacrit is required when swcompensate is 1."
        if self.swcompensate == 2:
            assert self.dcritrtz is not None, "dcritrtz is required when swcompensate is 2."


class Interception(PySWAPBaseModel):
    swinter: Literal[0, 1, 2]
    cofab: Optional[float] = Field(default=None, **UNITRANGE)
    table_intertb: Optional[Table] = None

    @model_validator(mode='after')
    def _validate_prepartion(self):
        if self.swinter == 1:
            assert self.cofab is not None, "cofab is required when swinter is 1."
        elif self.swinter == 1:
            assert self.table_intertb is not None, "table_intertb is required when swinter is 2."


class CO2Correction(PySWAPBaseModel):
    swco2: Literal[0, 1]
    atmofil: Optional[str]
    co2amaxtb: Optional[Arrays]
    co2efftb: Optional[Arrays]
    co2tratb: Optional[Arrays]

    @model_validator(mode='after')
    def _validate_co2correction(self):
        if self.swco2 == 1:
            assert self.atmofil is not None, 'amofil is required when swco2 is 1'
            assert self.co2amaxtb is not None, 'co2amaxtb is required when swco2 is 1'
            assert self.co2efftb is not None, 'co2efftb is required when swco2 is 1'
            assert self.co2tratb is not None, 'co2tratb is required when swco2 is 1'
