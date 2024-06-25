"""
Meteorological settings for SWAP simulations.

!!! note
    `Meteorology` object requires the `MetFile` object to be passed upon initialization. When the model is run,
    the `MetFile` object is saved to a .met file.

Classes:
    Meteorology: Holds the settings of the meteo section of the .swp file.
"""

from ..core.basemodel import PySWAPBaseModel
from ..core.fields import Table
from ..core.files import save_file
from ..core.valueranges import UNITRANGE
from .metfile import MetFile
from pydantic import Field, model_validator
from typing import Optional, Literal
from typing_extensions import Self


class Meteorology(PySWAPBaseModel):
    """Meteorological settings of the simulation.

    Attributes:
        lat (float): latitude of the meteo station [degrees].
        swetr (int): Switch type of weather data for potential evapotranspiration:

            * 0 - Use basic weather data and apply Penman-Monteith equation.
            * 1 - Use reference evapotranspiration data in combination with crop factors.

        swdivide (int): Switch for distribution of E and T. Defaults to 0:

            * 0 - Based on crop and soil factors.
            * 1 - Based on direct application of Penman-Monteith.

        swmetdetail (int): Switch for time interval of evapotranspiration and rainfall weather data:

            * 0 - Daily data.
            * 1 - Subdaily data.

        swrain (int): Switch for use of actual rainfall intensity, defaults to 0:

            * 0 - Use daily rainfall amounts.
            * 1 - Use daily rainfall amounts + mean intensity.
            * 2 - Use daily rainfall amounts + duration.
            * 3 - Use detailed rainfall records (dt < 1 day), as supplied in separate file.

        swetsine (int): Switch, distribute daily Tp and Ep according to sinus wave, default to 0:

            * 0 - No distribution.
            * 1 - Distribute Tp and Ep according to sinus wave.

        metfile (MetFile): MetFile model containing meteorological data to be saved to .met file.
        alt (float): Altitude of the meteo station [m].
        altw (float): Altitude of the wind [m].
        angstroma (float): Fraction of extraterrestrial radiation reaching the earth on overcast days.
        angstromb (float): Additional fraction of extraterrestrial radiation reaching the earth on clear days.
        table_rainflux (Table): rainfall intensity RAINFLUX as function of time TIME.
        rainfil (str): file name of file with detailed rainfall data.
        nmetdetail (int): Number of weather data records each day.

    Methods:
        write_met: Write the .met file.
    """

    # metfil: str
    lat: float = Field(ge=-90, le=90)
    swetr: Literal[0, 1]
    swdivide: Literal[0, 1]
    # TODO: SWRAIN should be optional, but Fortran code evaluates its presence anyway
    swrain: Optional[Literal[0, 1, 2, 3]] = 0
    # TODO: SWETSINE should be optional, but Fortran code evaluates its presence anyway
    swetsine: Literal[0, 1] = 0
    metfile: Optional[MetFile] = Field(
        default=None, repr=False)
    alt: float = Field(ge=-400.0, le=3000.0)
    altw: float = Field(default=None, ge=0.0, le=99.0)
    angstroma: float = Field(default=None, **UNITRANGE)
    angstromb: float = Field(default=None, **UNITRANGE)
    swmetdetail: Optional[Literal[0, 1]] = None
    table_rainflux: Optional[Table] = None
    rainfil: Optional[str] = None
    nmetdetail: Optional[int] = Field(default=None, ge=1, le=96)

    @model_validator(mode='after')
    def _validate_meteo_section(self) -> Self:

        if self.swetr == 1:  # if PM method is NOT used
            assert self.swetsine is not None, "SWETSINE is required when SWETR is 1"
            assert self.swrain is not None, "SWRAIN is required when SWETR is 1"
            if self.swrain == 1:
                assert self.table_rainflux is not None, "RAINFLUX is required when SWRAIN is 1"
            elif self.swrain == 3:
                assert self.rainfil, "RAINFIL is required when SWRAIN is 3"

        else:
            assert self.alt is not None, "alt settings are required when SWETR is 0"
            assert self.altw is not None, "altw settings are required when SWETR is 0"
            assert self.angstroma is not None, "angstroma settings are required when SWETR is 0"
            assert self.angstromb is not None, "angstromb settings are required when SWETR is 0"
            assert self.swmetdetail is not None, "SWMETDETAIL is required when SWETR is 0"
            if self.swmetdetail == 1:
                assert self.nmetdetail is not None, "NMETDETAIL is required when SWMETDETAIL is 1"

        return self

    def write_met(self, path: str):
        """Write the .met file.

        !!! note

            in this function the extension is not passed because
            swp file requires the metfile parameter to be passed already with 
            the extension.

        Parameters:
            path (str): Path to the file.
        """
        save_file(
            string=self.metfile.content.to_csv(
                index=False, lineterminator='\n'),
            fname=self.metfile.metfil,
            path=path
        )

        print(f'{self.metfile.metfil} saved.')
