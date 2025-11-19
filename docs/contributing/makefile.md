# Pixi Tasks

This project uses [Pixi](https://pixi.sh) for dependency management and task automation. Pixi provides a more modern, cross-platform alternative to Makefiles with built-in environment isolation.

## Available Tasks

Run any task with `pixi run <task-name>` or `pixi run -e <environment> <task-name>`:

### Development Tasks

- **test**: `pixi run test` - Run basic tests
- **test-cov**: `pixi run test-cov` - Run tests with coverage reporting
- **test-verbose**: `pixi run test-verbose` - Run tests with verbose output

### Code Quality

- **lint**: `pixi run lint` - Check code with ruff
- **lint-fix**: `pixi run lint-fix` - Auto-fix linting issues
- **format**: `pixi run format` - Format code with ruff
- **format-check**: `pixi run format-check` - Check if code is formatted
- **mypy**: `pixi run mypy` - Run static type checking
- **check-deps**: `pixi run check-deps` - Check for obsolete dependencies
- **check-all**: `pixi run check-all` - Run all quality checks
- **fix-all**: `pixi run fix-all` - Auto-fix formatting and linting

### Documentation

- **docs-serve**: `pixi run -e docs docs-serve` - Serve docs locally
- **docs-build**: `pixi run -e docs docs-build` - Build documentation
- **docs-deploy**: `pixi run -e docs docs-deploy` - Deploy docs to GitHub Pages

### Project Management

- **install-package**: `pixi run install-package` - Install package in development mode
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
