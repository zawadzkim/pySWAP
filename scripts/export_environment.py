"""Write environment.yml from the pixi `full` environment.

pixi is the default way to set up pySWAP for development. For users of
conda or an IDE that expects a conda environment, environment.yml holds the
same dependencies: the package itself (installed in editable mode) with the
test, dev and docs dependencies and all optional extras. Regenerate it after
changing dependencies in pyproject.toml:

    pixi run export-env
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "environment.yml"
HEADER = """\
# Conda environment for pySWAP development: the package (editable) with the
# test, dev and docs dependencies and all optional extras.
#   conda env create -f environment.yml && conda activate pyswap
# Generated from pyproject.toml by `pixi run export-env`; do not edit by hand.
"""


def main() -> int:
    pixi = shutil.which("pixi")
    if pixi is None:
        print(
            "pixi not found on PATH; install it from https://pixi.sh", file=sys.stderr
        )
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        exported = Path(tmp, "environment.yml")
        subprocess.run(
            [
                pixi,
                "workspace",
                "export",
                "conda-environment",
                "--environment",
                "full",
                "--name",
                "pyswap",
                str(exported),
            ],
            cwd=ROOT,
            check=True,
        )
        TARGET.write_text(HEADER + exported.read_text())
    print(f"Wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
