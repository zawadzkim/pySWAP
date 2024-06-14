"""tables for the soil-water module"""

from ..core.tablevalidation import BaseModel
from pandera.typing import Series
import pandera as pa
from typing import Optional

class INIPRESSUREHEAD(BaseModel):
    """Initial pressure head [cm, R] as a function of soil layer [1..N, I].

    Attributes:
        ZI: Series[int]: soil depth [-1.d5..0 cm, R].
        H: Series[float]: Initial soil water pressure head [-1.d10..1.d4 cm, R].
    """
    
    ZI: Series[int] = pa.Field(ge=-1.0e5, le=0.0)
    H: Series[float] = pa.Field(ge=-1.0e10, le=1.0e4)


class MXPONDTB(BaseModel):
    """minimum thickness for runoff PONDMXTB [0..1000 cm, R] as function of time
    
    Attributes:
        DATEPMX: Series[pa.DateTime]: Date of the ponding threshold for runoff.
        PONDMXTB: Series[float]: Minimum thickness for runoff.
    """
    DATEPMX: Series[pa.DateTime]
    PONDMXTB: Series[float]


class SOILPROFILE(BaseModel):
    """Vertical discretization of soil profile
    
    Attributes:
        ISUBLAY: Series[int]: number of sub layer, start with 1 at soil surface [1..MACP, I].
        ISOILLAY: Series[int]: number of soil physical layer, start with 1 at soil surface [1..MAHO, I].
        HSUBLAY: Series[float]: height of sub layer [0..1.d4 cm, R].
        HCOMP: Series[float]: height of compartments in the sub layer [0.0..1000.0 cm, R].
        NCOMP: Series[int]: number of compartments in the sub layer (Mind NCOMP = HSUBLAY/HCOMP) [1..MACP, I].
    """

    ISUBLAY: Series[int] = pa.Field(ge=1)
    ISOILLAY: Series[int] = pa.Field(ge=1)
    HSUBLAY: Series[float] = pa.Field(ge=0.0, le=1.0e4)
    HCOMP: Series[float] = pa.Field(ge=0.0, le=1.0e3)
    NCOMP: Series[int] = pa.Field(ge=1)

class SOILHYDRFUNC(BaseModel):
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
    ALFAW: Optional[Series[float]] = pa.Field(ge=0.0001, le=100.0)