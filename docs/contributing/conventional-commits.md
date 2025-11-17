# Conventional Commits Guide

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification to enable automated changelog generation.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

## Examples

### Features
```bash
feat: add support for SWAP version 4.3.0
feat(cli): add --in-place option to init command
feat(models)!: breaking change to Model API
```

### Bug Fixes
```bash
fix: handle missing crop parameters gracefully
fix(parser): resolve issue with date parsing in SWAP files
```

### Documentation
```bash
docs: add installation guide for Windows
docs(api): update docstrings for Model class
```

### Refactoring
```bash
refactor: simplify database connection logic
refactor(utils): extract common validation functions
```

## Breaking Changes

For breaking changes, add `!` after the type/scope:

```bash
feat!: change default output format to JSON
fix(api)!: remove deprecated methods
```

## Scopes

Common scopes in this project:
- `cli` - Command line interface
- `models` - Core model classes
- `utils` - Utility functions
- `parser` - File parsing logic
- `db` - Database operations
- `api` - Public API
- `docs` - Documentation
- `tests` - Test files

## Automated Processing

When you push to `main`, the following happens automatically:

1. **Changelog Generation**: Commits are analyzed and grouped by type
2. **Version Bumping**: Based on commit types (feat = minor, fix = patch, breaking = major)
3. **Release Creation**: GitHub release with generated changelog
4. **PyPI Publishing**: Package uploaded to PyPI

## Preview Changelog

Before pushing, you can preview what the changelog will look like:

```bash
python scripts/preview_changelog.py --since=v0.2.8
```