"""Tables for the irrigation settings.

Classes:

"""

import pandera as pa
from pandera.typing import Series

from ..core.tablevalidation import BaseTableModel


class IRRIGATION(BaseTableModel):
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
    IRDEPTH: Series[float] = pa.Field(ge=0.0, le=1000.0)
    IRCONC: Series[float] = pa.Field(ge=0.0, le=1000.0)
    IRTYPE: Series[int] = pa.Field(ge=0, le=1)
