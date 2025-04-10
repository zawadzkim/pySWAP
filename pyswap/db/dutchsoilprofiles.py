""" """

from numpy import arange, array, concatenate, diff, searchsorted
from pandas import concat
from pandera.typing import Series
from pydantic import BaseModel

from pyswap.components.tables import SOILHYDRFUNC, SOILPROFILE
from pyswap.core.io.io_csv import load_csv
from pyswap.libs import soilprofiles_dutch


class SoilProfile(BaseModel):
    """Class of a single soil profile.

    Attributes:
        bofek_cluster: Bofek cluster number.
        soilprofile_index: Soil profile index.
    """

    bofek_cluster: int | None = None
    soilprofile_index: int | None = None
    data: dict | None = None

    def plot(
        self,
    ):
        m = "Plotting of soil profiles is not implemented yet. "
        raise NotImplementedError(m)

    def get_swapinput_profile(
        self,
        discretisation_depths: list,
        discretisation_compheights: list,
    ):
        """Create a SOILPROFILE table.

        Parameters
        ----------
        discretisation_depths : list
            List of discretisation depths (cm).
            The depth of the profile is the total sum.
            If larger than 120 cm, the deepest soil physical layer will be extended.
        discretisation_compheights : list
            List of discretisation compartment heights (cm) for each discretisation depth.

        Example
        -------
        discretisation_depths = [50, 30, 60, 60, 100]
        discretisation_compheights = [1, 2, 5, 10, 20]
        will return a discretisation of:
            0-50 cm: 50 compartments of 1 cm
            50-80 cm: 15 compartments of 2 cm
            80-140 cm: 12 compartments of 5 cm
            140-200 cm: 6 compartments of 10 cm
            200-300 cm: 5 compartments of 20 cm
        The total depth of the profile is 300 cm.
        """

        # Get bottom of the soil physical layers
        zb_soillay = array(self.data["LAYER_ZBOTTOM"])

        # Get bottom of given discretisation layers
        zb_dislay = array(list(discretisation_depths)).cumsum()

        # Merge bottom discretisation and soil physical layers: sublayers
        zb_sublay = array(sorted(set(zb_soillay).union(set(zb_dislay))))

        # Remove values deeper than given depth (sum of discretisation keys)
        zb_sublay = zb_sublay[zb_sublay <= sum(discretisation_depths)]

        # Define the total amount of sublayers and their thickness
        isublay = arange(1, len(zb_sublay) + 1)
        hsublay = diff(concatenate(([0], zb_sublay)))

        # Define corresponding soil layer for each sublayer
        isoillay = searchsorted(zb_soillay, zb_sublay, side="left") + 1
        # Deeper sublayers than the BOFEK profile get same properties as the deepest soil physical layer
        isoillay[isoillay > len(zb_soillay)] = len(zb_soillay)

        # Find the height of the compartments in this soillayer, defined in discr
        hcomp = array(discretisation_compheights)[
            searchsorted(zb_dislay, zb_sublay, side="left")
        ]

        # Calculate the amount of compartments in each layer
        ncomp = (hsublay / hcomp).astype(int)

        # Create the SOILPROFILE table
        soilprofile_table = SOILPROFILE.create({
            "ISUBLAY": isublay,
            "ISOILLAY": isoillay,
            "HSUBLAY": hsublay,
            "HCOMP": hcomp,
            "NCOMP": ncomp,
        })

        return soilprofile_table

    def get_swapinput_hydraulic_params(
        self,
        ksatexm: Series[float] | None = None,
        h_enpr: Series[float] | None = None,
        bdens: Series[float] | None = None,
    ):
        """
        ksatexm : list
            List of measured saturated hydraulic conductivities (cm/d).
            If not provided, it will be set equal to ksatfit.
        h_enpr : list
            List of measured air entry pressure head (cm).
            If not provided, it will be set equal to 0.0 cm.
        bdens : list
            List of measured bulk densities (g/cm3).
            If not provided, it will be set equal to 1300 mg/cm3.
        """
        # Select the columns needed for the SOILHYDRFUNC table
        soilhydro_table = {
            param: values
            for param, values in self.data.items()
            if param
            in [
                "ORES",
                "OSAT",
                "ALFA",
                "NPAR",
                "KSATFIT",
                "LEXP",
            ]
        }

        # Set extra parameters to given or default values
        soilhydro_table["H_ENPR"] = h_enpr if h_enpr is not None else 0.0
        soilhydro_table["KSATEXM"] = (
            ksatexm if ksatexm is not None else soilhydro_table["KSATFIT"]
        )
        soilhydro_table["BDENS"] = bdens if bdens is not None else 1300.0

        # Create the SOILHYDRFUNC table
        return SOILHYDRFUNC.create(soilhydro_table)

    def get_swapinput_fractions():
        pass

    def get_swapinput_cofani(self):
        """
        Returns a list containing 1.0 for each soil physical layer.
        """
        return [1.0] * len(next(iter(self.data.values())))


class SoilProfilesDB(BaseModel):
    def get_profile(
        self,
        bofek_cluster: int | None = None,
        soilprofile_index: int | None = None,
    ) -> SoilProfile:
        """Returns Soilprofile object.

        Only one parameter should be given. If given a BOFEK number,
        the dominant profile will be filtered.

        Parameters
        ----------
        bofek_cluster : int
            Bofek cluster number.
        soilprofile_index : int
            Soil profile index.
        """

        # Check if only one input is given
        if sum([var is not None for var in [bofek_cluster, soilprofile_index]]) != 1:
            m = "Provide only one of the three parameters: bofek_cluster, soilprofile_index or soilprofile_code."
            raise ValueError(m)

        # Get table of profile
        profile_data = self.get_table_profiles(
            bofek_cluster=bofek_cluster,
            bofek_cluster_dominant=True,
            soilprofile_index=soilprofile_index,
        )
        # Convert to BaseTableModel
        profile_data = profile_data.to_dict("list")

        # Return Soilprofile object
        return SoilProfile(
            bofek_cluster=bofek_cluster,
            soilprofile_index=soilprofile_index,
            data=profile_data,
        )

    def get_table_profiles(
        self,
        bofek_cluster: int | list | None = None,
        bofek_cluster_dominant: bool = False,
        soilprofile_index: int | list | None = None,
        soilprofile_code: str | list | None = None,
    ):
        # Load library
        all_profiles = load_csv(soilprofiles_dutch)

        # For all indexes, find corresponding profiles if they exist
        profiles = []
        for params, column in zip(
            [bofek_cluster, soilprofile_index, soilprofile_code],
            ["CLUSTER_BOFEK", "SOILPROFILE_INDEX", "SOILPROFILE_CODE"],
            strict=False,
        ):
            # If params is not a list, make it a list
            params = [params] if not isinstance(params, list) else params
            # Find the corresponding profiles
            for par in params:
                # Check if the parameter value exists
                if par is not None and par in all_profiles[column].values:
                    # Get rows with matching profile
                    mask = all_profiles[column].values == par
                    # Adjust mask if Bofek and dominant profile in bofek are wanted
                    if bofek_cluster is not None and bofek_cluster_dominant:
                        mask = mask & all_profiles["CLUSTER_DOMINANT"]
                    matching_profile = all_profiles[mask]
                    profiles.append(matching_profile)

        # Check if there was a match, if not raise an error, else return one dataframe with all matches
        if profiles == []:
            m = f"""Provide a valid soil profile number ({soilprofile_index}),
                    soil profile code ({soilprofile_code})
                    or BOFEK cluster number ({bofek_cluster})."""
            raise ValueError(m)
        else:
            return concat(profiles)

    def plot_profiles():
        pass
