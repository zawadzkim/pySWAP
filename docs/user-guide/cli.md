# CLI Reference

pySWAP comes with a powerful command-line interface (CLI) that helps you scaffold projects, manage SWAP executables, and streamline your workflow.

## Installation

The CLI is automatically available after installing pySWAP:

```bash
pip install pyswap
```

## Commands Overview

### `pyswap init` - Project Scaffolding

Creates a well-structured project directory with modern dependency management.

```bash
pyswap init [OPTIONS]
```

**Options:**
- `--script/--no-script`: Include a Python script template (default: False)
- `--notebook/--no-notebook`: Include a Jupyter notebook template (default: True)
- `--pixi/--no-p ixi`: Include Pixi configuration for dependency management (default: True)

**Interactive Prompts:**
- Project name
- SWAP version used
- Author first/last name
- Your institution
- Your email address
- Any comments (optional)
- Folder name (defaults to project name)

**Generated Structure:**

With `--pixi` (default):
```text
your-project/
├── .git/                   # Git repository
├── .gitignore              # Git ignore rules
├── pixi.toml               # Pixi dependency management
├── README.md               # Project documentation with setup instructions  
├── __init__.py
├── data/                   # Data storage
├── models/                 # Your SWAP models
│   ├── __init__.py
│   └── main.ipynb         # Main notebook to get started
└── scripts/               # Helper scripts
    └── __init__.py
```

With `--no-pixi`:
```text
your-project/
├── .git/                   # Git repository
├── .gitignore              # Git ignore rules
├── README                  # Basic project documentation
├── __init__.py
├── data/                   # Data storage
├── models/                 # Your SWAP models
│   ├── __init__.py
│   └── main.ipynb         # Main notebook to get started
└── scripts/               # Helper scripts
    └── __init__.py
```

**Examples:**

```bash
# Create project with default settings (notebook + pixi)
pyswap init

# Create project with script instead of notebook
pyswap init --script --no-notebook

# Create project without pixi dependency management
pyswap init --no-pixi

# Create project with both script and notebook
pyswap init --script --notebook
```

### SWAP Executable Management

#### `pyswap get-swap` - Download SWAP Executable

Downloads and installs the SWAP executable for your platform.

```bash
pyswap get-swap [OPTIONS]
```

**Options:**
- `-v, --version TEXT`: SWAP version to download (default: "4.2.0")
- `-f, --force`: Force re-download even if executable exists
- `--verbose/--quiet`: Enable/disable verbose output (default: verbose)

**Examples:**

```bash
# Download latest SWAP version
pyswap get-swap

# Download specific version
pyswap get-swap --version 4.1.0

# Force re-download
pyswap get-swap --force

# Quiet download
pyswap get-swap --quiet
```

#### `pyswap upload-swap` - Install Local SWAP Executable

Install a SWAP executable from a local file.

```bash
pyswap upload-swap FILE_PATH VERSION [OPTIONS]
```

**Arguments:**
- `FILE_PATH`: Path to the SWAP executable file to install
- `VERSION`: Version identifier for the uploaded executable

**Options:**
- `-f, --force`: Force replace existing executable
- `--verbose/--quiet`: Enable/disable verbose output (default: verbose)

**Examples:**

```bash
# Install local SWAP executable
pyswap upload-swap ./my-swap-executable 4.2.1

# Force replace existing version
pyswap upload-swap ./swap-custom 4.2.1 --force
```

#### `pyswap check-swap` - Check SWAP Status

Verify if SWAP executable is available and working.

```bash
pyswap check-swap [OPTIONS]
```

**Options:**
- `--verbose/--quiet`: Enable/disable verbose output (default: verbose)

**Examples:**

```bash
# Check SWAP status
pyswap check-swap

# Quiet check (exit code only)
pyswap check-swap --quiet
```

#### `pyswap remove-swap` - Remove SWAP Executable

Remove the installed SWAP executable.

```bash
pyswap remove-swap [OPTIONS]
```

**Options:**
- `--verbose/--quiet`: Enable/disable verbose output (default: verbose)

**Examples:**

```bash
# Remove SWAP executable
pyswap remove-swap

# Quiet removal
pyswap remove-swap --quiet
```

#### `pyswap info` - Display System Information

Show information about pySWAP and SWAP setup.

```bash
pyswap info
```

## Workflow Examples

### Setting up a New Project

```bash
# 1. Create project with modern dependency management
pyswap init

# 2. Enter the project directory
cd your-project-name

# 3. Install dependencies with pixi
pixi install

# 4. Check if SWAP is working
pixi run testcase

# 5. Start working in Jupyter
pixi run jupyter
```

### Managing Multiple SWAP Versions

```bash
# Check current SWAP status
pyswap info

# Download specific version
pyswap get-swap --version 4.1.0

# Upload custom compiled version
pyswap upload-swap ./my-custom-swap 4.2.1-custom

# Switch back to official version
pyswap get-swap --version 4.2.0 --force

# Remove SWAP when done
pyswap remove-swap
```

## Integration with Development Tools

### Git Integration

All projects created with `pyswap init` automatically include:
- Git repository initialization
- Comprehensive `.gitignore` file
- Pixi-specific ignore patterns (when using `--pixi`)

### Pixi Integration

When using `--pixi` (default), projects include:
- `pixi.toml` with sensible defaults
- Pre-configured tasks (jupyter, test, testcase)
- Cross-platform dependency management
- Reproducible environments

## Troubleshooting

### Common Issues

**SWAP executable not found:**
```bash
pyswap check-swap
pyswap get-swap
```

**Project creation fails:**
- Ensure you have write permissions in the target directory
- Check that the project name doesn't contain invalid characters
- Verify Git is installed for repository initialization

**Pixi not working:**
- Install Pixi: `curl -fsSL https://pixi.sh/install.sh | bash`
- Restart your shell after installation
- Use `--no-pixi` if you prefer traditional dependency management

### Getting Help

```bash
# Show general help
pyswap --help

# Show help for specific command
pyswap init --help
pyswap get-swap --help

# Show version information
pyswap info
```