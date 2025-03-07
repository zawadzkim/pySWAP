# mypy: disable-error-code="call-overload, misc"


from typing import Literal as _Literal

from numpy import arange, array, concatenate, diff, searchsorted
from pydantic import (
    Field as _Field,
    PrivateAttr as _PrivateAttr,
)

from pyswap.components.tables import SOILHYDRFUNC, SOILPROFILE
from pyswap.core.basemodel import PySWAPBaseModel as _PySWAPBaseModel
from pyswap.core.fields import (
    Decimal2f as _Decimal2f,
    Decimal3f as _Decimal3f,
    String as _String,
    Table as _Table,
)
from pyswap.core.io.io_csv import load_csv
from pyswap.core.valueranges import UNITRANGE as _UNITRANGE
from pyswap.libs import soilprofiles
from pyswap.utils.mixins import (
    SerializableMixin as _SerializableMixin,
    YAMLValidatorMixin as _YAMLValidatorMixin,
)

__all__ = [
    "Evaporation",
    "SnowAndFrost",
    "SoilMoisture",
    "SoilProfile",
    "SurfaceFlow",
    "SOILPROFILE",
    "SOILHYDRFUNC",
]


class Evaporation(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Evaporation settings.

    Attributes:
        swcfbs (Literal[0, 1]): Switch for use of soil factor CFBS to calculate Epot from ETref.
        swredu (Literal[0, 1, 2]): Switch for the method for reduction of potential soil evaporation:

            * 0 - reduction to maximum Darcy flux.
            * 1 - reduction to maximum Darcy flux and to maximum Black (1969).
            * 2 - reduction to maximum Darcy flux and to maximum Boesten/Stroosnijder (1986).

        cfevappond (Optional[Decimal2f]): When ETref is used, evaporation coefficient in case of ponding [0..3].
        cfbs (Optional[Decimal2f]): Coefficient for potential soil evaporation [0.5..1.5].
        rsoil (Optional[Decimal2f]): Soil resistance of wet soil [0..1000.0].
        cofredbl (Optional[Decimal2f]): Soil evaporation coefficient of Black [0..1].
        rsigni (Optional[Decimal2f]): Minimum rainfall to reset method of Black [0..100].
        cofredbo (Optional[Decimal2f]): Soil evaporation coefficient of Boesten/Stroosnijder [0..1].
    """

    swcfbs: _Literal[0, 1] | None = None
    swredu: _Literal[0, 1, 2] | None = None
    cfevappond: _Decimal2f | None = _Field(default=None, ge=0, le=3)
    cfbs: _Decimal2f | None = _Field(default=None, ge=0.5, le=1.5)
    rsoil: _Decimal2f | None = _Field(default=None, ge=0, le=1000.0)
    cofredbl: _Decimal2f | None = _Field(default=None, **_UNITRANGE)
    rsigni: _Decimal2f | None = _Field(default=None, ge=0, le=100)
    cofredbo: _Decimal2f | None = _Field(default=None, **_UNITRANGE)


class SnowAndFrost(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Snow and frost settings for the model.

    Attributes:
        swsnow (Literal[0, 1]): Switch for calculation of
            snow accumulation and melt.
        swfrost (Literal[0, 1]): Switch, in case of frost reduce
            soil water flow.
        snowinco (Optional[Decimal2f]): Initial snow water equivalent [0..1000 cm].
        teprrain (Optional[Decimal2f]): Temperature above which all
            precipitation is rain [0..10 oC].
        teprsnow (Optional[Decimal2f]): Temperature below which all
            precipitation is snow [-10..0 oC].
        tfroststa (Optional[Decimal2f]): Soil temperature (oC) where reduction
            of water fluxes starts [-10.0..5.0 oC].
        tfrostend (Optional[Decimal2f]): Soil temperature (oC) where reduction
            of water fluxes ends [-10.0..5.0 oC].
    """

    swsnow: _Literal[0, 1] | None = None
    swfrost: _Literal[0, 1] | None = None
    snowinco: _Decimal2f | None = _Field(default=None, ge=0, le=1000)
    teprrain: _Decimal2f | None = _Field(default=None, ge=0, le=10)
    teprsnow: _Decimal2f | None = _Field(default=None, ge=-10, le=0)
    tfroststa: _Decimal2f | None = _Field(default=None, ge=-10, le=5)
    tfrostend: _Decimal2f | None = _Field(default=None, ge=-10, le=5)


class SoilMoisture(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Soil moisture content and water balance.

    Attributes:
        swinco (Literal[1, 2, 3]): Switch for the type of initial soil moisture condition:

            * 1 - pressure head as function of soil depth.
            * 2 - pressure head of each compartment is in
                hydrostatic equilibrium with initial groundwater level.
            * 3 - read final pressure heads from output file of previous
                Swap simulation.

        head_soildepth (Optional[Table]): Table with head and
            soil depth data.
        gwli (Optional[Decimal2f]): Initial groundwater level [-10000..100 cm].
        inifil (Optional[str]): name of output file *.END which contains
            initial values.
    """

    swinco: _Literal[1, 2, 3] | None = None
    head_soildepth: _Table | None = None
    gwli: _Decimal2f | None = _Field(default=None, ge=-10000, le=100)
    inifil: _String | None = None


class SoilProfile(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Vertical discretization of soil profile, soil hydraulic functions and
        hysteresis of soil water retention.

    Covers parts 4, 5, 6 and 7 of the .swp file.

    Attributes:
        swsophy (Literal[0, 1]): Switch for analytical functions or
            tabular it

            * 0 - Analytical functions with it of Mualem -
                van Genuchten parameters
            * 1 - Soil physical tables

        swhyst (Literal[0, 1, 2]): Hysteresis of soil water retention function

            * 0 - No hysteresis
            * 1 - Hysteresis, initial conditions wetting
            * 2 - Hysteresis, initial conditions drying

        filenamesophy (Optional[str]): Names of it files with
            soil hydraulic tables for each soil layer
        tau (Optional[Decimal2f]): Minimum pressure head difference to change
            wetting-drying [0..1000].
        swmacro (Literal[0, 1]): Switch for preferential flow due to macropores
        soilprofile (Table): Table with soil profile data
        soilhydrfunc (Optional[Table]): Table with
            soil hydraulic functions
    """

    _validation: bool = _PrivateAttr(default=False)

    swsophy: _Literal[0, 1] | None = None
    swhyst: _Literal[0, 1, 2] | None = None
    swmacro: _Literal[0, 1] | None = None
    filenamesophy: _String | None = None
    tau: _Decimal2f | None = _Field(default=None, ge=0, le=1000)
    soilprofile: _Table | None = None
    soilhydrfunc: _Table | None = None


class SurfaceFlow(_PySWAPBaseModel, _SerializableMixin, _YAMLValidatorMixin):
    """Surface flow settings (ponding, runoff and runon).

    Attributes:
        swpondmx (Literal[0, 1]): Switch for variation ponding
            threshold for runoff

            * 0 - Ponding threshold for runoff is constant
            * 1 - Ponding threshold for runoff varies in time

        swrunon (Literal[0, 1]): Switch for runon

            * 0 - No runon
            * 1 - Use runon data

        rsro (Optional[Decimal2f]): Drainage resistance for surface runoff [0.001..1.0].
        rsroexp (Optional[Decimal2f]): Exponent for drainage equation of surface runoff [0.01..10.0].
        pondmx (Optional[Decimal2f]): In case of ponding, minimum thickness for runoff [0..1000].
        rufil (Optional[str]): Name of the runon file.
        pondmxtb (Optional[Table]): Minimum thickness for runoff as a function of time.
    """

    swpondmx: _Literal[0, 1] | None = None
    swrunon: _Literal[0, 1] | None = None
    rsro: _Decimal3f | None = _Field(default=None, ge=0.001, le=1.0)
    rsroexp: _Decimal2f | None = _Field(default=None, ge=0.01, le=10.0)
    pondmx: _Decimal2f | None = _Field(default=None, ge=0, le=1000)
    rufil: _String | None = None
    pondmxtb: _Table | None = None


def soilprofile_from_Dutch_standards(
    bofek_cluster: int | None = None,
    soilprofile_ix: int | None = None,
) -> tuple[SOILPROFILE, SOILHYDRFUNC]:
    """Create a SOILPROFILE and SOILHYDRFUNC table from a BOFEK soil cluster or Dutch soil profile.

    !!! note:
        Parameters `bofek_cluster`, `soilprofile_nr` and `soilprofile_code` are checked sequentially
         for a value and the first defined parameter is used.
        This function returns a SOILPROFILE and SOILHYDRFUNC table with the following compartment heights:
            0-50 cm depth: 1 cm
            50-80 cm depth : 2 cm
            80-140 cm depth: 5 cm
            140-200 cm depth: 10 cm
            200-300 cm depth: 20 cm
        Layers deeper than the BOFEK profile get the same physical properties as the deepest layer.
        KSATEXM is set to KSATFIT.
        H_ENPR is set to 0.0.
        BDENS is set to 1300.0 mg/cm3.

    Parameters:
        bofek_cluster (int): BOFEK cluster number (default: None).
        soilprofile_nr (int): Soil profile number (default: None).

    Returns:
        SOILPROFILE: Soil profile table.
    """

    # Read library with profiles
    all_profiles = load_csv(soilprofiles)

    # Select profile by soilprofile index, code or BOFEK cluster, check if it exists
    if (bofek_cluster is not None) and (
        bofek_cluster in all_profiles["CLUSTER_BOFEK"].values
    ):
        mask = (all_profiles["CLUSTER_BOFEK"] == bofek_cluster) & (
            all_profiles["CLUSTER_DOMINANT"]
        )
        soilprofile = all_profiles.loc[mask]
    elif (soilprofile_ix is not None) and (
        soilprofile_ix in all_profiles["SOILPROFILE_INDEX"].values
    ):
        soilprofile = all_profiles.loc[
            all_profiles["SOILPROFILE_INDEX"] == soilprofile_ix
        ]
    else:
        m = f"""Provide a valid soil profile number ({soilprofile_ix})
                or BOFEK cluster number ({bofek_cluster})."""
        raise ValueError(m)

    # Get bottom of the soil physical layers
    zb_soillay = array(soilprofile["LAYER_ZBOTTOM"])
    # Define bottom and compartment height of the discretization layers
    discr = {50: 1, 80: 2, 140: 5, 200: 10, 300: 20}
    # Merge bottom discretisation and soil physical layers: sublayers
    zb_sublay = array(sorted(set(zb_soillay).union(discr.keys())))

    # Define the total amount of sublayers and their thickness
    isublay = arange(1, len(zb_sublay) + 1)
    hsublay = diff(concatenate(([0], zb_sublay)))

    # Define corresponding soil layer for each sublayer
    isoillay = searchsorted(zb_soillay, zb_sublay, side="left") + 1
    # Deeper sublayers than the BOFEK profile get same properties as the deepest soil physical layer
    isoillay[isoillay > len(zb_soillay)] = len(zb_soillay)

    # Find the height of the compartments in this soillayer, defined in discr
    hcomp = array(list(discr.values()))[
        searchsorted(array(list(discr.keys())), zb_sublay, side="left")
    ]

    # Calculate the amount of compartments in each layer
    ncomp = (hsublay / hcomp).astype(int)

    soilprofile_table = SOILPROFILE.create({
        "ISUBLAY": isublay,
        "ISOILLAY": isoillay,
        "HSUBLAY": hsublay,
        "HCOMP": hcomp,
        "NCOMP": ncomp,
    })

    # Get the soil hydraulic function parameters
    soilhydro_table = soilprofile_table[["ISOILLAY"]].join(
        soilprofile[
            ["LAYER", "ORES", "OSAT", "ALFA", "NPAR", "KSATFIT", "LEXP"]
        ].set_index("LAYER"),
        on="ISOILLAY",
        how="left",
    )
    # Set extra parameters to default values
    soilhydro_table["H_ENPR"] = 0.0
    soilhydro_table["KSATEXM"] = soilhydro_table["KSATFIT"]
    soilhydro_table["BDENS"] = 1300.0
    # Omit the ISOILLAY column
    soilhydro_table = soilhydro_table[soilhydro_table.columns[1:]]
    print(soilprofile_table, soilhydro_table)
    # Create the SOILHYDRFUNC table
    soilhydro_table = SOILHYDRFUNC.create(soilhydro_table.to_dict("list"))

    return (soilprofile_table, soilhydro_table)
