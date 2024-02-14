from dataclasses import dataclass, field
from ..core.utils.dtypes import Section, Subsection
from pandas import DataFrame


@dataclass
class SoilProfile(Subsection):
    """Vertical discretization of soil profile, soil hydraulic functions and hysteresis of soil water retention."""
    soilprofile: DataFrame
    swsophy: bool
    swhyst: int
    swmacro: bool
    filenamesophy: str | None = None,
    tau: float | None = None
    soilhydrfunc: DataFrame | None = None

    def __post_init__(self) -> None:

        if self.soilprofile is not None:
            assert "ISUBLAY" in self.soilprofile.columns, "ISUBLAY is required in soilprofile"
            assert "ISOILLAY" in self.soilprofile.columns, "ISOILLAY is required in soilprofile"
            assert "HSUBLAY" in self.soilprofile.columns, "HSUBLAY is required in soilprofile"
            assert "HCOMP" in self.soilprofile.columns, "HCOMP is required in soilprofile"
            assert "NCOMP" in self.soilprofile.columns, "NCOMP is required in soilprofile"

        if self.swsophy:
            assert self.soilhydrfunc is not None, "soilhydrfunc is required when swsophy is True"
            assert "ORES" in self.soilhydrfunc.columns, "ORES is required in soilhydrfunc"
            assert "OSAT" in self.soilhydrfunc.columns, "OSAT is required in soilhydrfunc"
            assert "ALFA" in self.soilhydrfunc.columns, "ALFA is required in soilhydrfunc"
            assert "NPAR" in self.soilhydrfunc.columns, "NPAR is required in soilhydrfunc"
            assert "KSATFIT" in self.soilhydrfunc.columns, "KSATFIT is required in soilhydrfunc"
            assert "LEXP" in self.soilhydrfunc.columns, "LEXP is required in soilhydrfunc"
            assert "ALFAW" in self.soilhydrfunc.columns, "ALFAW is required in soilhydrfunc"
            assert "H_ENPR" in self.soilhydrfunc.columns, "H_ENPR is required in soilhydrfunc"
            assert "KSATEXM" in self.soilhydrfunc.columns, "KSATEXM is required in soilhydrfunc"
            assert "BDENS" in self.soilhydrfunc.columns, "BDENS is required in soilhydrfunc"

        else:
            assert self.filenamesophy is not None, "filenamesophy is required when swsophy is True"

        if self.swhyst not in range(0, 3):
            raise ValueError("swhyst must be 0, 1, or 2")

        if self.swhyst in range(1, 3):
            assert self.tau is not None, "tau is required when swhyst is 1 or 2"
