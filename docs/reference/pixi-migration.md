# Pixi migration

We have changed the dependency and build management system from poetry to pixi. This documents brings some more detail why and what changes for developers.

## Overview

Pixi is a modern Python package management tool that uses conda-forge packages by default and provides better cross-platform compatibility and faster dependency resolution.

## Key Changes

### 1. Configuration File
- **Poetry**: `pyproject.toml` (build and dependency sections)
- **Pixi**: `pixi.toml` (complete project configuration)

### 2. Environment Management
- **Poetry**: Single virtual environment
- **Pixi**: Multiple environments (default, dev, docs, full)

### 3. Package Installation
- **Poetry**: PyPI packages only
- **Pixi**: Conda-forge packages (preferred) + PyPI packages (when needed)

## Commands Comparison

| Task | Poetry Command | Pixi Command |
|------|---------------|--------------|
| Install project | `poetry install` | `pixi install` |
| Install dev dependencies | `poetry install --extras dev` | `pixi install -e dev` |
| Run tests | `poetry run pytest` | `pixi run test` |
| Run with coverage | `poetry run pytest --cov` | `pixi run test-cov` |
| Format code | `poetry run ruff format` | `pixi run format` |
| Lint code | `poetry run ruff check` | `pixi run lint` |
| Type check | `poetry run mypy` | `pixi run mypy` |
| Build docs | `poetry run mkdocs serve` | `pixi run docs-serve` |
| Clean environment | `rm -rf .venv` | `pixi clean` |
| Add dependency | `poetry add package` | `pixi add package` |
| Remove dependency | `poetry remove package` | `pixi remove package` |

## Migration Steps

### 1. Install Pixi
```bash
curl -fsSL https://pixi.sh/install.sh | bash
# or
conda install -c conda-forge pixi
```

### 2. Initialize Project
The `pixi.toml` file has already been created with equivalent configuration.

### 3. Install Dependencies
```bash
# Install development environment with all features
pixi install -e full

# Or install specific environments
pixi install -e dev      # Development tools
pixi install -e docs     # Documentation tools
pixi install             # Default environment only
```

### 4. Update Development Workflow

#### Pre-commit Setup
```bash
pixi run dev-setup  # Installs pre-commit hooks and nbstripout
```

#### Testing
```bash
pixi run test           # Run tests
pixi run test-cov       # Run tests with coverage
pixi run test-verbose   # Run tests with verbose output
```

#### Code Quality
```bash
pixi run check-all      # Run all quality checks (lint, mypy, tests, deps)
pixi run fix-all        # Auto-fix formatting and linting issues
```

#### Documentation
```bash
pixi run docs-serve     # Serve docs locally
pixi run docs-build     # Build docs
pixi run docs-deploy    # Deploy to GitHub Pages
```

### 5. Environment Variables
If you have any environment variables in `.env` files that Poetry was using, they will still work with Pixi.

### 6. CI/CD Updates
All GitHub Actions workflows have been updated to use Pixi instead of Poetry:
- `tests.yaml`: Uses Pixi to run tests
- `deploy.yaml`: Uses Pixi for documentation deployment  
- `publish-to-pypi.yaml`: Uses Pixi for package building and publishing

## Benefits of Migration

### 1. Faster Dependency Resolution
- Uses conda-forge's pre-compiled packages
- Better dependency solver (conda-libmamba-solver)
- Parallel package downloads

### 2. Better Cross-Platform Support
- Consistent environments across Linux, macOS, and Windows
- Native binary packages reduce compilation issues
- Better handling of system dependencies

### 3. Multiple Environments
- Separate environments for different use cases
- Lighter default environment for production
- Full-featured development environment

### 4. Improved Reproducibility
- Lock files for exact version pinning
- Platform-specific dependency resolution
- Better isolation from system packages

## Troubleshooting

### 1. Missing Packages
If a package isn't available in conda-forge, it can be installed from PyPI using `pypi-dependencies` section in `pixi.toml`.

### 2. Version Conflicts
Pixi provides better error messages for dependency conflicts and suggests solutions.

### 3. Environment Issues
```bash
pixi clean              # Clean all environments
pixi install -e dev     # Reinstall development environment
```

### 4. Migration from Poetry Lock
Pixi will create new lock files based on the dependencies specified in `pixi.toml`. The old `poetry.lock` can be safely removed.

## Post-Migration Cleanup

After successful migration, you can remove Poetry-related files:
- `poetry.lock` (keep `pyproject.toml` for build metadata)
- Poetry sections in `pyproject.toml` can be removed if desired

## Package Building

The project still uses the standard Python packaging system (build + twine) for PyPI publishing. The `pyproject.toml` file retains the necessary build configuration.

## Backward Compatibility

The migration maintains full compatibility with existing:
- Test suites
- Documentation generation
- CI/CD pipelines
- Development workflows
- Package building and publishing