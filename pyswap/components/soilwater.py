import pandera as pa
from pandera.typing import Series
from pyswap.core.basemodel import PySWAPBaseModel
from pyswap.core.fields import String, Table
from pyswap.core.mixins import YAMLValidatorMixin, SerializableMixin


from typing import Literal

from pyswap.core.basemodel import BaseTableModel

__all__ = ["Evaporation", "SnowAndFrost", "SoilMoisture", "SoilProfile", "SurfaceFlow", "INIPRESSUREHEAD", "MXPONDTB", "SOILPROFILE", "SOILHYDRFUNC"]


class Evaporation(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Evaporation settings.

    Attributes:
        swcfbs (int): Switch for use of soil factor CFBS to calculate Epot
        from ETref swredu (int): Switch for the method for reduction of
        potential soil evaporation:

            * 0 - reduction to maximum Darcy flux.
            * 1 - reduction to maximum Darcy flux and to maximum Black (1969).
            * 2 - reduction to maximum Darcy flux and to maximum
                Boesten/Stroosnijder (1986).

        cfevappond (Optional[float]): hen ETref is used, evaporation
            coefficient in case of ponding.
        cfbs (Optional[float]): Coefficient for potential soil evaporation.
        rsoil (Optional[float]): Soil resistance of wet soil.
        cofredbl (Optional[float]): Soil evaporation coefficient of Black.
        rsigni (Optional[float]): Minimum rainfall to reset method of Black.
        cofredbo (Optional[float]): Soil evaporation coefficient of
            Boesten/Stroosnijder.
    """

    swcfbs: Literal[0, 1]
    swredu: Literal[0, 1, 2]
    cfevappond: float | None = None  # this is used if ETref is used
    cfbs: float | None = None
    rsoil: float | None = None
    cofredbl: float | None = None
    rsigni: float | None = None
    cofredbo: float | None = None


class SnowAndFrost(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow
        snowinco (Optional[float]): Initial snow water equivalent
        teprrain (Optional[float]): Temperature above which all
            precipitation is rain
        teprsnow (Optional[float]): Temperature below which all
            precipitation is snow
        snowcoef (Optional[float]): Snowmelt calibration factor
        tfroststa (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes starts
        tfrostend (Optional[float]): Soil temperature (oC) where reduction
            of water fluxes ends

    """

    swsnow: Literal[0, 1]
    swfrost: Literal[0, 1]
    snowinco: float | None = None
    teprrain: float | None = None
    teprsnow: float | None = None
    snowcoef: float | None = None
    tfrostst: float | None = None
    tfrostend: float | None = None


class SoilMoisture(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Soil moisture content and water balance.

    !!! warning
        swinco = 3 is not yet implemented. The model will run, but the output
        will not be retrieved.

    Attributes:
        swinco (int): Switch for the type of initial soil moisture condition:

            * 1 - pressure head as function of soil depth.
            * 2 - pressure head of each compartment is in
                hydrostatic equilibrium with initial groundwater level.
            * 3 - read final pressure heads from output file of previous
                Swap simulation.

        table_head_soildepth (Optional[Table]): Table with head and
            soil depth data.
        gwli (Optional[float]): Initial groundwater level [cm].
        inifil (Optional[str]): name of output file *.END which contains
            initial values.
    """

    swinco: Literal[1, 2, 3]
    table_head_soildepth: Table | None = None
    gwli: float | None = None
    inifil: String | None = None


class SoilProfile(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Vertical discretization of soil profile, soil hydraulic functions and
        hysteresis of soil water retention.

    Covers parts 4, 5, 6 and 7 of the .swp file.

    Attributes:
        swsophy (Literal[0, 1]): Switch for analytical functions or
            tabular input

            * 0 - Analytical functions with input of Mualem -
                van Genuchten parameters
            * 1 - Soil physical tables

        swhyst (Literal[0, 1, 2]): Hysteresis of soil water retention function

            * 0 - No hysteresis
            * 1 - Hysteresis, initial conditions wetting
            * 2 - Hysteresis, initial conditions drying

        filenamesophy (Optional[str]): Names of input files with
            soil hydraulic tables for each soil layer
        tau (Optional[float]): Minimum pressure head difference to change
            wetting-drying
        swmacro (Literal[0, 1]): Switch for preferential flow due to macropores
        table_soilprofile (Table): Table with soil profile data
        table_soilhydrfunc (Optional[Table]): Table with
            soil hydraulic functions
    """

    swsophy: Literal[0, 1]
    swhyst: Literal[0, 1, 2]
    swmacro: Literal[0, 1]
    filenamesophy: String | None = None
    tau: float | None = None
    table_soilprofile: Table
    table_soilhydrfunc: Table | None = None


class SurfaceFlow(PySWAPBaseModel, SerializableMixin, YAMLValidatorMixin):
    """Surface flow settings (ponding, runoff and runon).

    Attributes:
        swpondmx (Literal[0, 1]): Switch for variation ponding
            threshold for runoff

            * 0 - Ponding threshold for runoff is constant
            * 1 - Ponding threshold for runoff varies in time

        swrunon (Literal[0, 1]): Switch for runon

            * 0 - No runon
            * 1 - Use runon data

        rsro (float): Drainage resistance for surface runoff
        rsroexp (float): Exponent for drainage equation of surface runoff
        pondmx (Optional[float]): In case of ponding, minimum
            thickness for runoff
        rufil (Optional[str]): Name of the runon file
        table_pondmxtb (Optional[Table]): Minimum thickness for runoff as
            a function of time
    """

    swpondmx: Literal[0, 1]
    swrunon: Literal[0, 1]
    rsro: float = 0.5
    rsroexp: float = 1.0
    pondmx: float | None = None
    rufil: String | None = None
    table_pondmxtb: Table | None = None


class INIPRESSUREHEAD(BaseTableModel):
    """Initial pressure head [cm, R] as a function of soil layer [1..N, I].

    Attributes:
        ZI: Series[int]: soil depth [-1.d5..0 cm, R].
        H: Series[float]: Initial soil water pressure head [-1.d10..1.d4 cm, R].
    """

    ZI: Series[int] = pa.Field(ge=-1.0e5, le=0.0)
    H: Series[float] = pa.Field(ge=-1.0e10, le=1.0e4)


class MXPONDTB(BaseTableModel):
    """minimum thickness for runoff PONDMXTB [0..1000 cm, R] as function of time

    Attributes:
        DATEPMX: Series[pa.DateTime]: Date of the ponding threshold for runoff.
        PONDMXTB: Series[float]: Minimum thickness for runoff.
    """

    DATEPMX: Series[pa.DateTime]  # type: ignore
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

    ISUBLAY: Series[int] = pa.Field(ge=1)
    ISOILLAY: Series[int] = pa.Field(ge=1)
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