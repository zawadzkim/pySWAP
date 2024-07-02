"""Tables for the crop settings

Classes:
    RDTB: Root depth table
"""
from ..core.tablevalidation import BaseModel
from ..core import UNITRANGE, DVSRANGE, YEARRANGE
from pandera.typing import Series
import pandera as pa


class RDTB(BaseModel):
    """Rooting Depth [0..1000 cm, R], as a function of development stage [0..2 -, R].

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RD (Series[float]): Rooting depth of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RD: Series[float] = pa.Field(ge=0.0, le=100.0)


class RDCTB(BaseModel):
    """List root density [0..100 cm/cm3, R] as function of relative rooting depth [0..1 -, R]

    Attributes:
        RRD (Series[float]): Relative rooting depth of the crop.
        RDENS (Series[float]): Root density of the crop.

    """
    RRD: Series[float] = pa.Field(ge=0.0, le=100.0)
    RDENS: Series[float] = pa.Field(**UNITRANGE)


class GCTB(BaseModel):
    """Leaf Area Index [0..12 (m2 leaf)/(m2 soil), R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        LAI (Series[float]): Leaf Area Index of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    LAI: Series[float] = pa.Field(ge=0.0, le=12.0)


class CHTB(BaseModel):
    """Crop Height [0..1.d4 cm, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        CH (Series[float]): Crop height of the crop.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    CH: Series[float] = pa.Field(ge=0.0, le=1.0e4)


class KYTB(BaseModel):
    """Yield response factor [0..5 -, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        KY (Series[float]): Yield response factor of the crop.
    """
    DVS: Series[float] = pa.Field(**DVSRANGE)
    KY: Series[float] = pa.Field(ge=0.0, le=5.0)


class MRFTB(BaseModel):
    """Ratio root total respiration / maintenance respiration [1..5.0 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        MAX_RESP_FACTOR (Series[float]): Ratio root total respiration / maintenance respiration.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    MAX_RESP_FACTOR: Series[float] = pa.Field(ge=1.0, le=5.0)


class WRTB(BaseModel):
    """dry weight of roots at soil surface [0..10 kg/m3, R], as a function of development stage [0..2 -,R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        W_ROOT_SS (Series[float]): Dry weight of roots at soil surface.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    W_ROOT_SS: Series[float] = pa.Field(ge=0.0, le=10.0)


class CROPROTATION(BaseModel):
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
class DTSMTB(BaseModel):
    """increase in temperature sum [0..60 oC, R] as function of daily average temperature [0..100 oC, R]

    Attributes:
        TAV (Series[float]): Daily average temperature.
        DTSM (Series[float]): Increase in temperature sum.
    """

    TAV: Series[float] = pa.Field(ge=0.0, le=100.0)
    DTSM: Series[float] = pa.Field(ge=0.0, le=60.0)


class SLATB(BaseModel):
    """leaf area [0..1 ha/kg, R] as function of crop development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        SLA (Series[float]): Leaf area.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB(BaseModel):
    """maximum CO2 assimilation rate [0..100 kg/ha/hr, R] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        AMAX (Series[float]): Maximum CO2 assimilation rate.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    AMAX: Series[float] = pa.Field(ge=0.0, le=100.0)


class TMPFTB(BaseModel):
    """reduction factor of AMAX [-, R] as function of average day temperature [-10..50 oC, R]

    Attributes:
        TAVD (Series[float]): Minimum temperature.
        TMPF (Series[float]): Reduction factor of AMAX.
    """

    TAVD: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMPF: Series[float] = pa.Field(ge=0.0, le=1.0)


class TMNFTB(BaseModel):
    """reduction factor of AMAX [-, R] as function of minimum day temperature [-10..50 oC, R]

    Attributes:
        TMNR (Series[float]): Minimum temperature.
        TMNF (Series[float]): Reduction factor of AMAX.
    """

    TMNR: Series[float] = pa.Field(ge=-10.0, le=50.0)
    TMNF: Series[float] = pa.Field(ge=0.0, le=1.0)


class RFSETB(BaseModel):
    """reduction factor of senescence [-, R] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RFSE (Series[float]): Reduction factor of senescence.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RFSE: Series[float] = pa.Field(ge=0.0, le=1.0)


class FRTB(BaseModel):
    """fraction of total dry matter increase partitioned to the roots [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FR: Series[float] = pa.Field(ge=0.0, le=1.0)


class FLTB(BaseModel):
    """fraction of total above ground dry matter increase partitioned to the leaves [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FL: Series[float] = pa.Field(ge=0.0, le=1.0)


class FSTB(BaseModel):
    """fraction of total above ground dry matter increase partitioned to the stems [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FS: Series[float] = pa.Field(ge=0.0, le=1.0)


class FOTB(BaseModel):
    """fraction of total above ground dry matter increase partitioned to the storage organs [kg/kg, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        FO (Series[float]): Fraction of total above ground dry matter increase partitioned to the storage organs.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    FO: Series[float] = pa.Field(ge=0.0, le=1.0)


class RDRRTB(BaseModel):
    """relative death rates of roots [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RDRR (Series[float]): Relative death rates of roots.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB(BaseModel):
    """relative death rates of stems [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DVS (Series[float]): Development stage of the crop.
        RDRS (Series[float]): Relative death rates of stems.
    """

    DVS: Series[float] = pa.Field(**DVSRANGE)
    RDRS: Series[float] = pa.Field(ge=0.0)


class DMGRZTB(BaseModel):
    """threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger grazing as function of daynumber [1..366 d, R]

    Attributes:
        DNR (Series[float]): Day number.
        DMGRZ (Series[float]): Dry matter growth rate of roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMGRZ: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class LSDATB(BaseModel):
    """Actual livestock density of each grazing period

    !!! note

        total number of periods should be equal to number of periods in SEQGRAZMOW

    Attributes:
        SEQNR (Series[int]): number of the sequence period with mowing/grazing [0..366 d, I]
        LSDA (Series[float]): Actual Live Stock Density of the grazing period [0.0..1000.0 LS/ha, R]
    """

    SEQNR: Series[int] = pa.Field(**YEARRANGE)
    LSDA: Series[float] = pa.Field(ge=0.0, le=1000.0)


class LSDBTB(BaseModel):
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


class RLWTB(BaseModel):
    """rooting depth RL [0..5000 cm, R] as function of root weight RW [0..5000 kg DM/ha, R]

    Attributes:
        RW (Series[float]): rooting depth
        RL (Series[float]): root weight
    """

    RW: Series[float] = pa.Field(ge=0.0, le=5000.0)
    RL: Series[float] = pa.Field(ge=0.0, le=5000.0)


class DMMOWTB(BaseModel):
    """List threshold of above ground dry matter [0..1d6 kg DM/ha, R] to trigger mowing as function of daynumber [1..366 d, R]

    !!! note

        maximum 20 records


    Attributes:
        DNR (Series[float]): Day number.
        DMMOW (Series[float]): threshold of above ground dry matter [0..1d6 kg DM/ha, R]
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    DMMOW: Series[float] = pa.Field(ge=0.0, le=1.0e6)


class DMMOWDELAY(BaseModel):
    """Relation between dry matter harvest [0..1d6 kg/ha, R] and days of delay in regrowth [0..366 d, I] after mowing

    Attributes:
        DMMOWDELAY (Series[float]): Dry matter harvest [0..1d6 kg/ha, R]
        DAYDELAY (Series[int]): days of delay in regrowth [0..366 d, I]
    """

    DMMOWDELAY: Series[float] = pa.Field(ge=0.0, le=1.0e6)
    DAYDELAY: Series[int] = pa.Field(**YEARRANGE)


class CHTB_GRASS(BaseModel):
    """Crop Height [0..1.d4 cm, R], as function of dev. stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): day number.
        CH (Series[float]): Crop height of the crop.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    CH: Series[float] = pa.Field(ge=0.0, le=1.0e4)


class SLATB_GRASS(BaseModel):
    """leaf area [0..1 ha/kg, R] as function of crop development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        SLA (Series[float]): Leaf area.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    SLA: Series[float] = pa.Field(ge=0.0, le=1.0)


class AMAXTB_GRASS(BaseModel):
    """maximum CO2 assimilation rate [0..100 kg/ha/hr, R] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        AMAX (Series[float]): Maximum CO2 assimilation rate.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    AMAX: Series[float] = pa.Field(ge=0.0, le=100.0)


class RFSETB_GRASS(BaseModel):
    """reduction factor of senescence [-, R] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RFSE (Series[float]): Reduction factor of senescence.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RFSE: Series[float] = pa.Field(**UNITRANGE)


class FRTB_GRASS(BaseModel):
    """fraction of total dry matter increase partitioned to the roots [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FR (Series[float]): Fraction of total dry matter increase partitioned to the roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FR: Series[float] = pa.Field(**UNITRANGE)


class FLTB_GRASS(BaseModel):
    """fraction of total above ground dry matter increase partitioned to the leaves [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FL (Series[float]): Fraction of total above ground dry matter increase partitioned to the leaves.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FL: Series[float] = pa.Field(**UNITRANGE)


class FSTB_GRASS(BaseModel):
    """fraction of total above ground dry matter increase partitioned to the stems [kg/kg, R]

    Attributes:
        DNR (Series[float]): Day number.
        FS (Series[float]): Fraction of total above ground dry matter increase partitioned to the stems.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    FS: Series[float] = pa.Field(**UNITRANGE)


class RDRRTB_GRASS(BaseModel):
    """relative death rates of roots [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RDRR (Series[float]): Relative death rates of roots.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RDRR: Series[float] = pa.Field(ge=0.0)


class RDRSTB_GRASS(BaseModel):
    """relative death rates of stems [kg/kg/d] as function of development stage [0..2 -, R]

    Attributes:
        DNR (Series[float]): Day number.
        RDRS (Series[float]): Relative death rates of stems.
    """

    DNR: Series[float] = pa.Field(**YEARRANGE)
    RDRS: Series[float] = pa.Field(ge=0.0)
