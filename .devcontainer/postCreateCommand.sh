#! /usr/bin/env bash
git config --global --add safe.directory /workspaces/$(basename $(pwd))

pipx install poetry
poetry config virtualenvs.in-project true
poetry install

# Install the Jupyter kernel for this environment
poetry run python -m ipykernel install --user --name=pyswap --display-name "Python (pyswap)"

# Install pre-commit hooks
poetry run pre-commit install --install-hooks

mkdir -p .logs
