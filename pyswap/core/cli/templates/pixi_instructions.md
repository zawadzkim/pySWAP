## Environment Setup with Pixi

This project uses [Pixi](https://pixi.sh) for dependency management. Pixi is a fast, cross-platform package manager built on top of conda-forge.

### Installation

If you don't have Pixi installed yet:

**Linux/macOS:**
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows:**
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

Or visit [pixi.sh](https://pixi.sh) for more installation options.

### Usage

1. **Install dependencies:**
   ```bash
   pixi install
   ```

2. **Run Jupyter Lab:**
   ```bash
   pixi run jupyter
   ```

3. **Run tests:**
   ```bash
   pixi run test
   ```

### Available Tasks

- `pixi run jupyter`: Start Jupyter Lab
- `pixi run test`: Run pytest