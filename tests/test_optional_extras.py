"""pySWAP works without its optional extras; features that need one say which.

Each check runs in a fresh interpreter with the extra's package blocked
(sys.modules[name] = None makes `import name` raise ImportError), so the
test does not depend on what is installed and does not reload modules in
the test process.
"""

import subprocess
import sys
import textwrap


def _run_without(packages: str, code: str) -> subprocess.CompletedProcess:
    blocked = "".join(f"sys.modules[{name!r}] = None\n" for name in packages.split(","))
    script = "import sys\n" + blocked + textwrap.dedent(code)
    return subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, check=False
    )


def test_pyswap_imports_without_knmi():
    result = _run_without("knmi", "import pyswap\nimport pyswap.components\n")
    assert result.returncode == 0, result.stderr


def test_metfile_from_knmi_names_the_extra():
    result = _run_without(
        "knmi",
        """
        from pyswap.components import metfile_from_knmi
        try:
            metfile_from_knmi(metfil="x.met", stations="260")
        except ImportError as e:
            print(e)
        """,
    )
    assert result.returncode == 0, result.stderr
    assert 'pip install "pyswap[knmi]"' in result.stdout


GIS_PACKAGES = "pyproj,shapely,shapely.geometry"


def test_location_and_meteorology_work_without_gis():
    result = _run_without(
        GIS_PACKAGES,
        """
        import pyswap
        from pyswap.components import Meteorology
        from pyswap.gis import Location

        loc = Location(lat=52.0, lon=21.0, alt=10.0)
        meteo = Meteorology(
            meteo_location=loc, swetr=0, swdivide=1, swmetdetail=0,
            altw=10.0, angstroma=0.25, angstromb=0.5,
        )
        assert float(meteo.lat) == 52.0 and float(meteo.alt) == 10.0
        meteo = Meteorology(
            lat=52.0, alt=10.0, swetr=0, swdivide=1, swmetdetail=0,
            altw=10.0, angstroma=0.25, angstromb=0.5,
        )
        """,
    )
    assert result.returncode == 0, result.stderr


def test_gis_features_name_the_extra():
    result = _run_without(
        GIS_PACKAGES,
        """
        from pyswap.gis import Location

        loc = Location(lat=52.0, lon=21.0, alt=10.0)
        for call in (lambda: loc.to_crs("EPSG:31370"), lambda: loc.point,
                     lambda: Location(lat=1, lon=1, alt=0, crs="EPSG:31370")):
            try:
                call()
            except ImportError as e:
                print(e)
        """,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.count('pip install "pyswap[gis]"') == 3
