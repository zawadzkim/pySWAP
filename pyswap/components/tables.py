# pyright: reportInvalidTypeForm=false

from typing import Literal

import pandera.pandas as pa
from pandera.typing import Series

from pyswap.core.basemodel import BaseTableModel
from pyswap.core.valueranges import DVSRANGE, UNITRANGE, YEARRANGE

__all__ = [
    "AMAXTB",
    "CFTB",
    "CO2AMAXTB",
    "CO2EFFTB",
    "CO2TRATB",
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
    "LSDATB",
    "LSDBTB",
    "MRFTB",
    "RDCTB",
    "RDRRTB",
    "RDRSTB",
    "RDTB",
    "RFSETB",
    "RLWTB",
    "SHORTINTERVALMETEODATA",
    "SLATB",
    "TMNFTB",
    "TMPFTB",
    "WRTB",
]  #  TODO: needs update?

# %% ++++++++++++++++++++++++++++ CROP TABLES ++++++++++++++++++++++++++++

crop_tables = [
    "DATEHARVEST",
    "RDTB",
    "RDCTB",
    "GCTB",
    "CFTB",
    "INTERTB",
    "KYTB",
    "MRFTB",
    "WRTB",
    "CROPROTATION",
    "DTSMTB",
    "SLATB",
    "AMAXTB",
    "TMPFTB",
    "TMNFTB",
    "RFSETB",
    "FRTB",
    "FLTB",
    "FSTB",
    "FOTB",
    "RDRRTB",
    "RDRSTB",
    "DMGRZTB",
    "LSDATB",
    "LSDBTB",
    "RLWTB",
    "DMMOWTB",
    "DMMOWDELAY",
    "IRRIGEVENTS",
    "TC1TB",
    "TC2TB",
    "TC3TB",
    "TC4TB",
    "TC7TB",
    "TC8TB",
    "DC1TB",
    "DC2TB",
    "CO2EFFTB",
    "CO2TRATB",
    "CO2AMAXTB",
    "LSDA",
]


class DATEHARVEST(BaseTableModel):
    """Date of harvest

    Attributes:
        DATEHARVEST (Series[pa.DateTime]): Date of harvest.
    """

    DATEHARVEST: Series[pa.DateTime]


class RDTB(BaseTableModel):
    """Rooting Depth [0..1000 cm, R], as a function of development stage [0..2 -, R].

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RD (Series[float]): Rooting depth of the crop.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
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


class CFTB(BaseTableModel):
    """Crop factor [0..2 [-], R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        DNR (Series[float]): Day number.
        CF (Series[float]): Crop factor.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    CF: Series[float] | None


class CHTB(BaseTableModel):
    """Crop Height [0..1.d4 cm, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        DNR (Series[float]): Day number.
        CH (Series[float]): Crop height.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    # # CF was added for compatibility with example grass files in original SWAP distribution
    # # that are used for testing this package. CF is only stated but not used there. I
    # removed it because it was conflicting with other settings. Input files for the examples
    # should be adjusted.
    CH: Series[float] | None


class INTERTB(BaseTableModel):
    """Interception parameters for closed forest canopies (SWINTER=2).

    Attributes:
        T (Series[int]): Time [0..366 d, R].
        PFREE (Series[float]): Free throughfall coefficient [0..1 -, R].
        PSTEM (Series[float]): Stem flow coefficient [0..1 -, R].
        SCANOPY (Series[float]): Storage capacity of canopy [0..10 cm, R].
        AVPREC (Series[float]): Average rainfall intensity [0..100 cm/d, R].
        AVEVAP (Series[float]): Average evaporation intensity during rainfall from a wet canopy [0..10 cm/d, R].
    """

    T: Series[float] = pa.Field(ge=0, le=366)
    PFREE: Series[float] = pa.Field(ge=0.0, le=1.0)
    PSTEM: Series[float] = pa.Field(ge=0.0, le=1.0)
    SCANOPY: Series[float] = pa.Field(ge=0.0, le=10.0)
    AVPREC: Series[float] = pa.Field(ge=0.0, le=100.0)
    AVEVAP: Series[float] = pa.Field(ge=0.0, le=10.0)


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

    CROPSTART: Series[pa.DateTime]
    CROPEND: Series[pa.DateTime]
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
    """Specific leaf area [0..1 ha/kg, R] as function of crop development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        SLA (Series[float]): Leaf area.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB(BaseTableModel):
    """maximum CO2 assimilation rate [0..100 kg/ha/hr, R] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        AMAX (Series[float]): Maximum CO2 assimilation rate.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
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

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RFSE: Series[float] = pa.Field(ge=0.0, le=1.0)


class FRTB(BaseTableModel):
    """fraction of total dry matter increase partitioned to the roots [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    FR: Series[float] = pa.Field(ge=0.0, le=1.0)


class FLTB(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the leaves [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    FL: Series[float] = pa.Field(ge=0.0, le=1.0)


class FSTB(BaseTableModel):
    """fraction of total above ground dry matter increase partitioned to the stems [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
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

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB(BaseTableModel):
    """relative death rates of stems [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RDRS (Series[float]): Relative death rates of stems.
    """

    DVS: Series[float] | None = pa.Field(**DVSRANGE)
    DNR: Series[float] | None = pa.Field(**YEARRANGE)
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

    LSDb: Series[float] = pa.Field(ge=0.0, le=1000.0)
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


class IRRIGEVENTS(BaseTableModel):
    """information for each fixed irrigation event.

    Attributes:
        IRDATE (Series[datetime]):date of irrigation.
        IRDEPTH (Series[float]): amount of water [0..1000 mm, R].
        IRCONC (Series[float]): concentration of irrigation water [0..1000 mg/cm3, R].
        IRTYPE (Series[int]): type of irrigation

            * 0 - sprinkling
            * 1 - surface

    """

    IRDATE: Series[pa.DateTime]
    IRDEPTH: Series[float] | None = pa.Field(default=None, ge=0.0, le=1000.0)
    IRCONC: Series[float] = pa.Field(ge=0.0, le=1000.0)
    IRTYPE: Series[int] = pa.Field(ge=0, le=1)


class TC1TB(BaseTableModel):
    """tc1tb option table"""

    DVS_TC1: Series[float] = pa.Field(ge=0.0, le=2.0)
    TREL: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC2TB(BaseTableModel):
    """tc2tb option table"""

    DVS_TC2: Series[float] = pa.Field(ge=0.0, le=2.0)
    RAW: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC3TB(BaseTableModel):
    """tc3tb option table"""

    DVS_TC3: Series[float] = pa.Field(ge=0.0, le=2.0)
    TAW: Series[float] = pa.Field(ge=0.0, le=1.0)


class TC4TB(BaseTableModel):
    """tc4tb option table"""

    DVS_TC4: Series[float] = pa.Field(ge=0.0, le=2.0)
    DWA: Series[float] = pa.Field(ge=0.0, le=500.0)


class TC7TB(BaseTableModel):
    """tc7tb option table"""

    DVS_TC7: Series[float] = pa.Field(ge=0.0, le=2.0)
    HCRI: Series[float] = pa.Field(ge=-1000.0, le=-100.0)


class TC8TB(BaseTableModel):
    """tc8tb option table"""

    DVS_TC8: Series[float] = pa.Field(ge=0.0, le=2.0)
    TCRI: Series[float] = pa.Field(ge=0.0, le=1.0)


class DC1TB(BaseTableModel):
    DVS_DC1: Series[float]
    DI: Series[float]


class DC2TB(BaseTableModel):
    DVS_DC2: Series[float]
    FID: Series[float]


class CO2EFFTB(BaseTableModel):
    """Correction factor light use efficiency for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


class CO2TRATB(BaseTableModel):
    """Correction factor maximum transpiration rate for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


class CO2AMAXTB(BaseTableModel):
    """Correction factor assimilation rate for change in CO2 concentration."""

    CO2PPM: Series[float]
    FACTOR: Series[float]


class VERNRTB(BaseTableModel):
    """Vernalization rate as a function of average air temperature."""

    TAV: Series[float]
    VERNRATE: Series[float]


class LSDA(BaseTableModel):
    """Actual livestock density of each grazing period

    !!! note

        total number of periods should be equal to number of periods in SEQGRAZMOW

    Attributes:
        SEQNR (Series[int]): number of the sequence period with mowing/grazing [0..366 d, I]
        LSDA (Series[float]): Actual Live Stock Density of the grazing period [0.0..1000.0 LS/ha, R]
    """

    SEQNR: Series[int] = pa.Field(**YEARRANGE)
    LSDA: Series[float] = pa.Field(ge=0.0, le=1000.0)


# %% ++++++++++++++++++++++++++++ METEO TABLES ++++++++++++++++++++++++++++

meteo_tables = [
    "DAILYMETEODATA",
    "SHORTINTERVALMETEODATA",
    "DETAILEDRAINFALL",
    "RAINFLUX",
]


class DAILYMETEODATA(BaseTableModel):
    """Format detailed daily meteo data.

    TODO:
    format decimals in the variables.
    """

    STATION: Series[str]
    DD: Series[str]
    MM: Series[str]
    YYYY: Series[str]
    RAD: Series[float]
    TMIN: Series[float]
    TMAX: Series[float]
    HUM: Series[float]
    WIND: Series[float]
    RAIN: Series[float]
    ETREF: Series[float]
    WET: Series[float]


class SHORTINTERVALMETEODATA(BaseTableModel):
    Date: Series[pa.DateTime]
    Record: Series[int] = pa.Field(ge=1, le=10)
    Rad: Series[float]
    Temp: Series[float]
    Hum: Series[float]
    Wind: Series[float]
    Rain: Series[float]


class DETAILEDRAINFALL(BaseTableModel):
    Station: Series[str]
    Day: Series[int]
    Month: Series[int]
    Year: Series[int]
    Time: Series[float]
    Amount: Series[float]


class RAINFLUX(BaseTableModel):
    TIME: Series[float] = pa.Field(**YEARRANGE)
    RAINFLUX: Series[float] = pa.Field(ge=0, le=1000.0)


# %% ++++++++++++++++++++++++++++ SOILWATER TABLES ++++++++++++++++++++++++++++

soilwater_tables = [
    "INIPRESSUREHEAD",
    "MXPONDTB",
    "SOILPROFILE",
    "SOILHYDRFUNC",
    "SOILTEXTURES",
    "INITSOILTEMP",
]


class INIPRESSUREHEAD(BaseTableModel):
    """Initial pressure head [cm, R] as a function of soil layer [1..N, I].

    Attributes:
        ZI: Series[int]: soil depth [-1.d5..0 cm, R].
        H: Series[float]: Initial soil water pressure head [-1.d10..1.d4 cm, R].
    """

    ZI: Series[float] = pa.Field(ge=-1.0e5, le=0.0)
    H: Series[float] = pa.Field(ge=-1.0e10, le=1.0e4)


class MXPONDTB(BaseTableModel):
    """minimum thickness for runoff PONDMXTB [0..1000 cm, R] as function of time

    Attributes:
        DATEPMX: Series[pa.DateTime]: Date of the ponding threshold for runoff.
        PONDMXTB: Series[float]: Minimum thickness for runoff.
    """

    DATEPMX: Series[pa.DateTime]
    PONDMXTB: Series[float]


class SOILPROFILE(BaseTableModel):
    """Vertical discretization of soil profile

    Attributes:
        ISUBLAY: Series[int]: number of sub layer, start with 1 at soil surface [1..MACP, I].
        ISOILLAY: Series[int]: number of soil physical layer, start with 1 at soil surface [1..MAHO, I].
        HSUBLAY: Series[float]: height of sub layer [0..1.d4 cm, R].
        HCOMP: Series[float]: height of compartments in the sub layer [0.0..1000.0 cm, R].
        NCOMP: Series[int]: number of compartments in the sub layer (Mind NCOMP = HSUBLAY/HCOMP) [1..MACP, I].
    """

    ISOILLAY: Series[int] = pa.Field(ge=1)
    ISUBLAY: Series[int] = pa.Field(ge=1)
    HSUBLAY: Series[float] = pa.Field(ge=0.0, le=1.0e4)
    HCOMP: Series[float] = pa.Field(ge=0.0, le=1.0e3)
    NCOMP: Series[int] = pa.Field(ge=1)


class SOILHYDRFUNC(BaseTableModel):
    """Soil hydraulic functions table.

        !!! warning
            ALFAW required only when the hysteresis option is set to 1 or 2. This column is set as optional column and (for now) is not checked.

    Attributes:
        ORES (Series[float]): Residual water content [0..1 cm3/cm3, R]
        OSAT (Series[float]): Saturated water content [0..1 cm3/cm3, R]
        ALFA (Series[float]): Parameter alfa of main drying curve [0.0001..100 /cm, R]
        NPAR (Series[float]): Parameter n [1.001..9 -, R]
        LEXP (Series[float]): Exponent in hydraulic conductivity function [-25..25 -, R]
        KSATFIT (Series[float]): Fitting parameter Ksat of hydraulic conductivity function [1.d-5..1d5 cm/d, R]
        H_ENPR (Series[float]): Air entry pressure head [-40.0..0.0 cm, R]
        KSATEXM (Series[float]): Measured hydraulic conductivity at saturated conditions [1.d-5..1d5 cm/d, R]
        BDENS (Series[float]): Dry soil bulk density [100..1d4 mg/cm3, R]
        ALFAW (Optional[Series[float]]): Alfa parameter of main wetting curve in case of hysteresis [0.0001..100 /cm, R]
    """

    ORES: Series[float] = pa.Field(ge=0.0, le=1.0)
    OSAT: Series[float] = pa.Field(ge=0.0, le=1.0)
    ALFA: Series[float] = pa.Field(ge=0.0001, le=100.0)
    NPAR: Series[float] = pa.Field(ge=1.001, le=9.0)
    LEXP: Series[float] = pa.Field(ge=-25.0, le=25.0)
    KSATFIT: Series[float] = pa.Field(ge=1.0e-5, le=1.0e5)
    H_ENPR: Series[float] = pa.Field(ge=-40.0, le=0.0)
    KSATEXM: Series[float] = pa.Field(ge=1.0e-5, le=1.0e5)
    BDENS: Series[float] = pa.Field(ge=100.0, le=1.0e4)
    ALFAW: Series[float] | None = pa.Field(ge=0.0001, le=100.0)


# %% ++++++++++++++++++++++++++++ HEAT FLOW TABLES ++++++++++++++++++++++++++++


class SOILTEXTURES(BaseTableModel):
    """Table for soil textures.

    Attributes:
        PSAND (float): Depth of soil layer [cm, R]
        PSILT (float): Sand content [g/g mineral parts, R]
        PCLAY (float): Clay content [g/g mineral parts, R]
        ORGMAT (float): Organic matter content [g/g dry soil, R]
    """

    PSAND: float
    PSILT: float
    PCLAY: float
    ORGMAT: float


class INITSOILTEMP(BaseTableModel):
    """Table for initial soil temperature.

    Attributes:
        ZH (float): Depth of soil layer [cm, R]
        TSOIL (float): Initial temperature [oC, R]
    """

    ZH: float = pa.Field(ge=-100000, le=0)
    TSOIL: float = pa.Field(ge=-50, le=50)


# %% ++++++++++++++++++++++++++++ BOUNDARY TABLES ++++++++++++++++++++++++++++

boundary_tables = [
    "GWLEVEL",
    "QBOT2",
    "HAQUIF",
    "QBOT4",
    "QTAB",
    "HBOT5",
    "DATET",
    "CSEEPARR",
    "INISSOIL",
    "MISC",
]


class GWLEVEL(BaseTableModel):
    """Table for groundwater levels.

    Attributes:
        DATE (Series[pa.DateTime]): Date of the groundwater level.
        GWLEVEL (Series[float]): Groundwater level.
    """

    DATE1: Series[pa.DateTime]
    GWLEVEL: Series[float]


class QBOT2(BaseTableModel):
    """Table for bottom boundary flow.

    Attributes:
        DATE2 (Series[pa.DateTime]): Date of the bottom boundary flow.
        QBOT2 (Series[float]): Bottom boundary flow.
    """

    DATE2: Series[pa.DateTime]
    QBOT2: Series[float]


class HAQUIF(BaseTableModel):
    """Table for aquifer thickness.

    Attributes:
        DATE3 (Series[pa.DateTime]): Date of the aquifer thickness.
        HAQUIF (Series[float]): Aquifer thickness.
    """

    DATE3: Series[pa.DateTime]
    HAQUIF: Series[float]


class QBOT4(BaseTableModel):
    """Table for bottom boundary flow.

    Attributes:
        DATE4 (Series[pa.DateTime]): Date of the bottom boundary flow.
        QBOT4 (Series[float]): Bottom boundary flow.
    """

    DATE4: Series[pa.DateTime]
    QBOT4: Series[float]


class QTAB(BaseTableModel):
    """Table for height of the water table.

    Attributes:
        HTAB (Series[pa.DateTime]): Date of the height of the water table.
        HTABLE (Series[float]): Height of the water table.
    """

    HTAB: Series[float]
    QTAB: Series[float]


class HBOT5(BaseTableModel):
    """Table for bottom compartment pressure head.

    Attributes:
        DATE6 (Series[pa.DateTime]): Date of the bottom compartment pressure head.
        HBOT5 (Series[float]): Bottom compartment pressure head.
    """

    DATE5: Series[pa.DateTime]
    HBOT5: Series[float]


class DATET(BaseTableModel):
    """Table for time.

    Attributes:
        DATE7 (Series[pa.DateTime]): Date of the time.
        TIME (Series[float]): Time.
    """

    DATET: Series[pa.DateTime]
    TBOT: Series[float]


class CSEEPARR(BaseTableModel):
    """Table for seepage.

    Attributes:
        DATE8 (Series[pa.DateTime]): Date of the seepage.
        CSEEPARR (Series[float]): Seepage.
    """

    DATEC: Series[pa.DateTime]
    CSEEPARR: Series[float]


class INISSOIL(BaseTableModel):
    """Table for capillary rise.

    Attributes:
        DATE9 (Series[pa.DateTime]): Date of the capillary rise.
        CML (Series[float]): Capillary rise.
    """

    ZC: Series[float]
    CML: Series[float]


class MISC(BaseTableModel):
    """Table for miscellaneous.

    Attributes:
        DATE10 (Series[pa.DateTime]): Date of the miscellaneous.
        MISC (Series[float]): Miscellaneous.
    """

    LDIS: Series[float]
    KF: Series[float]
    DECPOT: Series[float]
    FDEPTH: Series[float]


# %% ++++++++++++++++++++++++++++ DRAINAGE TABLES ++++++++++++++++++++++++++++

drainage_tables = [
    "DRNTB",
    "DRAINAGELEVELTOPPARAMS",
    "DATOWLTB1",
    "DATOWLTB2",
    "DATOWLTB3",
    "DATOWLTB4",
    "DATOWLTB5",
    "SECWATLVL",
    "MANSECWATLVL",
    "QWEIR",
    "QWEIRTB",
    "PRIWATLVL",
    "QDRNTB",
]


class DRNTB(BaseTableModel):
    """Drainage characteristics table.

    Attributes:
        LEV (Series[int]): Drainage level [1..5, I].
        SWDTYP (Series[int]): Type of drainage medium: 1 = drain tube, 2 = open channel.
        L (Series[float]): Drain spacing [1..100000 m, R].
        ZBOTDRE (Series[float]): Level of drainage medium bottom [-10000..0 cm, R].
        GWLINF (Series[float]): Groundwater level influence [-10000..200 cm, R].
        RDRAIN (Series[float]): Drainage resistance [10..1d5 d, R].
        RINFI (Series[float]): Infiltration resistance [0..1d5 d, R].
        RENTRY (Series[float]): Entry resistance [0..1000 d, R].
        REXIT (Series[float]): Exit resistance [0..1000 d, R].
        WIDTHR (Series[float]): Width of the drainage medium [0..1000 cm, R].
        TALUDR (Series[float]): Talud of the drainage medium [0..1000 cm, R].
    """

    LEV: Series[int] = pa.Field(ge=1, le=5)
    SWDTYP: Series[Literal[0, 1]]
    L: Series[float] = pa.Field(ge=1.0, le=100000.0)
    ZBOTDRE: Series[float]
    GWLINF: Series[float] = pa.Field(ge=-1000.0, le=0.0)
    RDRAIN: Series[float] = pa.Field(ge=1.0, le=100000.0)
    RINFI: Series[float] = pa.Field(ge=1.0, le=100000.0)
    RENTRY: Series[float] = pa.Field(ge=0.0, le=100.0)
    REXIT: Series[float] = pa.Field(ge=0.0, le=100.0)
    WIDTHR: Series[float] = pa.Field(ge=0.0, le=10000.0)
    TALUDR: Series[float] = pa.Field(ge=0.01, le=5.0)


class DRAINAGELEVELTOPPARAMS(BaseTableModel):
    """Drainage level top parameters table.

    I couldn't find the description of this table. It occurs in the swa.dra file
    of the Hupselbrook example, but not in the templates.

    Attributes:
        SWTOPDISLAY (Series[Literal[0, 1]]): Switch for each drainage level to distribute drainage flux vertically with a given position of the top of the model discharge layers [Y=1, N=0]
        ZTOPDISLAY (Series[float]): Array with depth of top of model discharge layer for each drain level [-10000.0..0.0, cm, R]
        FTOPDISLAY (Series[float]): Array with factor of top of model discharge layer for each drain level [0.0..1.0, -, R]
    """

    SWTOPDISLAY: Series[Literal[0, 1]]
    ZTOPDISLAY: Series[float] = pa.Field(ge=-10000.0, le=0.0)
    FTOPDISLAY: Series[float] = pa.Field(ge=0.0, le=1.0)


class DATOWLTB1(BaseTableModel):
    """Table for drainage water level.

    Attributes:
        DATOWL1 (Series[pa.DateTime]): Date of the drainage water level.
        WLEVEL (Series[float]): Drainage water level.
    """

    DATOWL1: Series[pa.DateTime]
    LEVEL1: Series[float]


class DATOWLTB2(BaseTableModel):
    """Table for drainage water level.

    Attributes:
        DATOWL2 (Series[pa.DateTime]): Date of the drainage water level.
        LEVEL2 (Series[float]): Drainage water level.
    """

    DATOWL2: Series[pa.DateTime]
    LEVEL2: Series[float]


class DATOWLTB3(BaseTableModel):
    """Table for drainage water level.

    Attributes:
        DATOWL3 (Series[pa.DateTime]): Date of the drainage water level.
        LEVEL3 (Series[float]): Drainage water level.
    """

    DATOWL3: Series[pa.DateTime]
    LEVEL3: Series[float]


class DATOWLTB4(BaseTableModel):
    """Table for drainage water level.

    Attributes:
        DATOWL4 (Series[pa.DateTime]): Date of the drainage water level.
        LEVEL4 (Series[float]): Drainage water level.
    """

    DATOWL4: Series[pa.DateTime]
    LEVEL4: Series[float]


class DATOWLTB5(BaseTableModel):
    """Table for drainage water level.

    Attributes:
        DATOWL5 (Series[pa.DateTime]): Date of the drainage water level.
        LEVEL5 (Series[float]): Drainage water level.
    """

    DATOWL5: Series[pa.DateTime]
    LEVEL5: Series[float]


class SECWATLVL(BaseTableModel):
    DATE2: Series[pa.DateTime]
    WLS: Series[float]


class MANSECWATLVL(BaseTableModel):
    IMPER_4B: Series[float]
    IMPEND: Series[pa.DateTime]
    SWMAN: Series[float]
    WSCAP: Series[float]
    WLDIP: Series[float]
    INTWL: Series[float]


class QWEIR(BaseTableModel):
    IMPER_4C: Series[float]
    HBWEIR: Series[float]
    ALPHAW: Series[float]
    BETAW: Series[float]


class QWEIRTB(BaseTableModel):
    IMPER_4D: Series[float]
    IMPTAB: Series[float]
    HTAB: Series[float]
    QTAB: Series[float]


class PRIWATLVL(BaseTableModel):
    DATE1: Series[pa.DateTime]
    WLP: Series[float]


class QDRNTB(BaseTableModel):
    QDRAIN: Series[float]
    GWL: Series[float]


# %% ++++++++++++++++++++++++++++ GENERAL SETTINGS TABLES ++++++++++++++++++++++++++++

general_settings_tables = ["OUTDATIN", "OUTDAT"]


class OUTDATIN(BaseTableModel):
    """OUTDATIN table

    Attributes:
        OUTDAT: Series[str]: Name of the output file.
    """

    OUTDATIN: Series[pa.DateTime]


class OUTDAT(BaseTableModel):
    """OUTDAT table

    Attributes:
        OUTDAT: Series[str]: Name of the output file.
    """

    OUTDAT: Series[pa.DateTime]
