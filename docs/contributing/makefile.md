# Development environment and Pixi tasks

This project uses [Pixi](https://pixi.sh) for dependency management and task automation. Pixi provides a more modern, cross-platform alternative to Makefiles with built-in environment isolation.

## Setting up a development environment

**pixi (default).** Clone the repository with its submodules and install the development environment, which contains the package (editable) and the test and lint tools:

```shell
git clone --recurse-submodules https://github.com/zawadzkim/pySWAP.git
cd pySWAP
pixi install -e dev
pixi run -e dev test
```

Tasks run in the `default` environment unless you name another one with `-e`. The default environment holds only the package and its core dependencies, so run the tests and code checks in the `dev` environment (`pixi run -e dev test`, `pixi run -e dev lint`) and the documentation tasks in `docs`. The environments are:

| Environment | Contents |
|-------------|----------|
| `default` | pySWAP and its core dependencies |
| `test` | + pytest and the optional extras |
| `dev` | + test, lint, type-checking and build tools, and the optional extras |
| `docs` | + MkDocs and its plugins, and the optional extras |
| `full` | dev + docs |

To use the environment in your IDE, select the interpreter in `.pixi/envs/dev` (in VS Code: *Python: Select Interpreter*).

**conda (alternative).** `environment.yml` in the repository root lists the same dependencies as the `full` pixi environment (the package in editable mode with all test, dev and docs dependencies and extras):

```shell
conda env create -f environment.yml
conda activate pyswap
pytest
```

`environment.yml` is generated from `pyproject.toml` with `pixi run export-env`; regenerate it whenever dependencies change instead of editing it by hand.

## Available Tasks

Run any task with `pixi run -e <environment> <task-name>` (without `-e`, tasks run in the `default` environment). Tests and code checks need the `dev` environment, documentation tasks the `docs` environment:

### Development Tasks

- **test**: `pixi run -e dev test` - Run basic tests
- **test-cov**: `pixi run -e dev test-cov` - Run tests with coverage reporting
- **test-verbose**: `pixi run -e dev test-verbose` - Run tests with verbose output

### Code Quality

- **lint**: `pixi run -e dev lint` - Check code with ruff
- **lint-fix**: `pixi run -e dev lint-fix` - Auto-fix linting issues
- **format**: `pixi run -e dev format` - Format code with ruff
- **format-check**: `pixi run -e dev format-check` - Check if code is formatted
- **mypy**: `pixi run -e dev mypy` - Run static type checking
- **check-deps**: `pixi run -e dev check-deps` - Check for obsolete dependencies
- **check-all**: `pixi run -e dev check-all` - Run all quality checks
- **fix-all**: `pixi run -e dev fix-all` - Auto-fix formatting and linting

### Documentation

- **docs-serve**: `pixi run -e docs docs-serve` - Serve docs locally
- **docs-build**: `pixi run -e docs docs-build` - Build documentation
- **docs-versions**: `pixi run -e docs docs-versions` - List the deployed documentation versions. Versions are deployed by CI with mike: `dev` on every push to the dev branch, the minor version (e.g. `0.3`) with the `latest` alias on release.

### Project Management

- **install-package**: `pixi run install-package` - Install package in development mode
- **export-env**: `pixi run export-env` - Regenerate `environment.yml` (conda alternative) from `pyproject.toml`
- **clean-cache**: `pixi run clean-cache` - Clean pytest/mypy caches
- **clean-build**: `pixi run clean-build` - Clean build artifacts
- **clean-all**: `pixi run clean-all` - Clean everything

### Pre-commit

- **pre-commit-install**: `pixi run pre-commit-install` - Install pre-commit hooks
- **pre-commit-run**: `pixi run pre-commit-run` - Run pre-commit on all files

## Environment-Specific Tasks

Pixi supports multiple environments for different use cases:

- **default**: Core dependencies only
- **dev**: Development tools (testing, linting, etc.)
- **docs**: Documentation building
- **full**: All dependencies combined

Example: `pixi run -e dev test-cov` runs tests with coverage in the dev environment.

## Why Pixi Instead of Make?

- **Cross-platform**: Works identically on Windows, macOS, and Linux
- **Environment isolation**: Each task runs with the correct dependencies
- **Integrated dependency management**: No need to manage separate virtual environments
- **Modern tooling**: Built-in support for conda-forge and PyPI packages
- **No duplication**: Single source of truth in `pixi.toml`

You are welcome to add new tasks to `pixi.toml` when contributing to the project!
