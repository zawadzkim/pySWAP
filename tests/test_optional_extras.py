"""pySWAP works without its optional extras; features that need one say which.

Each check runs in a fresh interpreter with the extra's package blocked
(sys.modules[name] = None makes `import name` raise ImportError), so the
test does not depend on what is installed and does not reload modules in
the test process.
"""

import subprocess
import sys
import textwrap


def _run_without(package: str, code: str) -> subprocess.CompletedProcess:
    script = f"import sys\nsys.modules[{package!r}] = None\n" + textwrap.dedent(code)
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
