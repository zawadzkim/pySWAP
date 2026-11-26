#!/usr/bin/env bash
set -euo pipefail

git config --global --add safe.directory "$(pwd)"

# The WOFOST crop parameters are a git submodule.
git submodule update --init --recursive

# pixi manages the environments (see pyproject.toml).
curl -fsSL https://pixi.sh/install.sh | bash
export PATH="$HOME/.pixi/bin:$PATH"

pixi install -e dev

# Jupyter kernel for the notebooks.
pixi run -e dev python -m ipykernel install --user --name pyswap --display-name "Python (pyswap)"

