from pyswap.core.metadata import Metadata
from pyswap.core.simsettings import SimSettings
from datetime import date as dt

meta = Metadata(author="John Doe",
                institution="University of Somewhere",
                email="john.doe@somewhere.com",
                project_name="Test",
                swap_ver="4.0")

simset = SimSettings(
    swerror=0,
    swyrvar=0,
    tstart='2002-01-01',
    tend='2004-12-31',
    nprintday=1,
    swmonth=1,
    period=1,
    swres=0,
    swodat=0,
    outdat=['2002-01-31', '2004-12-31'],
    datefix='2004-12-31',
    inlist_csv=['rain', 'evap'],
    dznew=[0.13452, 0.2345, 0.333]
)
