"""
Meteorological settings for SWAP simulations.

!!! note
    `Meteorology` object requires the `MetFile` object to be passed upon
    initialization. When the model is run, the `MetFile` object is
    saved to a .met file.

Classes:
    Meteorology: Holds the settings of the meteo section of the .swp file.
"""

from decimal import Decimal
from pydantic import Field, model_validator, field_validator
from ..core import PySWAPBaseModel, SerializableMixin, Table, String, UNITRANGE
from ..simsettings import MeteoLocation
from .metfile import MetFile
from ..core.mixins import YAMLValidatorMixin


class Meteorology(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Meteorological settings of the simulation.

    !! note
        SWRAIN and SWETSINE should be optional,
        but Fortran code evaluates its presence anyway. They are set to
        0 by default.


    Attributes:
        lat (Decimal): latitude of the meteo station [degrees].
        swetr (int): Switch type of weather data for
            potential evapotranspiration:

            * 0 - Use basic weather data and apply Penman-Monteith equation.
            * 1 - Use reference evapotranspiration data in combination with
                crop factors.

        swdivide (int): Switch for distribution of E and T. Defaults to 0:

            * 0 - Based on crop and soil factors.
            * 1 - Based on direct application of Penman-Monteith.

        swmetdetail (int): Switch for time interval of evapotranspiration and
            rainfall weather data:

            * 0 - Daily data.
            * 1 - Subdaily data.

        swrain (int): Switch for use of actual rainfall intensity,
            defaults to 0:

            * 0 - Use daily rainfall amounts.
            * 1 - Use daily rainfall amounts + mean intensity.
            * 2 - Use daily rainfall amounts + duration.
            * 3 - Use detailed rainfall records (dt < 1 day), as supplied in
                separate file.

        swetsine (int): Switch, distribute daily Tp and Ep according to
            sinus wave, default to 0:

            * 0 - No distribution.
            * 1 - Distribute Tp and Ep according to sinus wave.

        metfile (MetFile): MetFile model containing meteorological data to
            be saved to .met file.
        alt (Decimal): Altitude of the meteo station [m].
        altw (Decimal): Altitude of the wind [m].
        angstroma (Decimal): Fraction of extraterrestrial radiation reaching
            the earth on overcast days.
        angstromb (Decimal): Additional fraction of extraterrestrial radiation
            reaching the earth on clear days.
        table_rainflux (Table): rainfall intensity RAINFLUX as function
            of time TIME.
        rainfil (str): file name of file with detailed rainfall data.
        nmetdetail (int): Number of weather data records each day.

    Properties:
        met: Returns the string representation of the met file.

    Methods:
        write_met: Writes the .met file.
    """

    lat: Optional[Decimal] = Field(default=None, ge=-90, le=90)
    meteo_location: Optional[Location] = Field(default=None, exclude=True)
    swetr: Literal[0, 1]
    swdivide: Literal[0, 1]
    swrain: Literal[0, 1, 2, 3] | None = 0
    swetsine: Literal[0, 1] = 0
    metfile: Optional[MetFile] = Field(default=None, repr=False)
    alt: Decimal = Optional[Field(default=None, ge=-400.0, le=3000.0)]
    altw: Decimal = Field(default=None, ge=0.0, le=99.0)
    angstroma: Decimal = Field(default=None, **UNITRANGE)
    angstromb: Decimal = Field(default=None, **UNITRANGE)
    swmetdetail: Literal[0, 1] | None = None
    table_rainflux: Table | None = None
    rainfil: String | None = None
    nmetdetail: int | None = Field(default=None, ge=1, le=96)

    @property
    def met(self):
        return self.metfile.content.to_csv(index=False, lineterminator="\n")

    @field_validator("altw", "angstroma", "angstromb")
    def set_decimals(cls, v):
        return v.quantize(Decimal("0.00"))
    
    def model_post_init(self, __context):
        """Set lat, and alt from `meteo_location` if they are not provided."""
        if self.meteo_location:
            self.lat = self.meteo_location.lat
            self.alt = self.meteo_location.alt
         
    def write_met(self, path: str):
        """Write the .met file.

        !!! note

            in this function the extension is not passed because
            swp file requires the metfile parameter to be passed already with
            the extension.

        Parameters:
            path (str): Path to the file.
        """

        self.metfile.save_file(string=self.met, fname=self.metfile.metfil, path=path)

        print(f"{self.metfile.metfil} saved.")
