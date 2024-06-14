"""Tables for the crop settings

Classes:
    RDTB: Root depth table
"""
from ..core.tablevalidation import BaseModel
from ..core import UNITRANGE, DVSRANGE
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