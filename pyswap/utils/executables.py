"""
SWAP executable management module.

This module provides functionality to download and manage SWAP executables
similar to how flopy handles MODFLOW executables.
"""

import os
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional

import pyswap
from pyswap.core.defaults import IS_WINDOWS
import typer

import yaml


def get_swap_executable_path() -> Path:
    """Get the path where SWAP executable should be installed."""
    # Use the package installation directory
    package_dir = Path(pyswap.__file__).parent
    exe_dir = package_dir / "libs" / "swap"
    
    # make a directory if it doesn't exist
    exe_dir.mkdir(parents=True, exist_ok=True)

    exe_path = exe_dir / ("swap.exe" if IS_WINDOWS else "swap420")
    
    return exe_path

def write_version_info(version: str):
    version_file = get_swap_executable_path().parent / "version.yaml"
    version_data = {"version_swap": version}
    with version_file.open("w") as f:
        yaml.dump(version_data, f)

def read_swap_version() -> Optional[str]:
    """Read the SWAP version from the version file."""
    version_file = get_swap_executable_path().parent / "version.yaml"
    if version_file.exists():
        try:
            with version_file.open("r") as f:
                data = yaml.safe_load(f)
                return data.get("version_swap")
        except Exception:
            return None
    return None

def show_info(verbose: bool = True) -> dict:
    """Display information about pySWAP and SWAP versions and installation.
    
    Args:
        verbose: Whether to print the information to stdout. Defaults to True.
        
    Returns:
        Information dictionary with version and status details.
    
    Examples:
        >>> import pyswap as psp
        >>> info = psp.show_info()
        pySWAP version: 0.2.8
        SWAP version: 4.2.0
        SWAP executable: Available at /path/to/swap420
        
        >>> # Get info without printing
        >>> info = psp.show_info(verbose=False)
        >>> print(f"Running pySWAP {info['pyswap_version']}")
    """
    import pyswap
    
    # Get pySWAP version
    pyswap_version = pyswap.__version__
    
    # Get SWAP version and executable info
    swap_version = read_swap_version()
    swap_exe_path = get_swap_executable_path()
    swap_available = swap_exe_path.exists() and os.access(swap_exe_path, os.X_OK)
    
    # Get platform info
    system = "Windows" if IS_WINDOWS else "Linux"
    
    info = {
        "pyswap_version": pyswap_version,
        "swap_version": swap_version,
        "swap_executable_path": str(swap_exe_path),
        "swap_available": swap_available,
        "platform": system,
        "package_location": str(Path(pyswap.__file__).parent)
    }
    
    if verbose:
        typer.echo(f"pySWAP Setup Information:")
        typer.echo(f"  pySWAP version: {pyswap_version}")
        if swap_version:
            typer.echo(f"  SWAP version: {swap_version}")
        else:
            typer.echo(f"  SWAP version: Not installed")
        
        if swap_available:
            typer.echo(f"  SWAP executable: ✓ Available at {swap_exe_path}")
        else:
            typer.echo(f"  SWAP executable: ✗ Not found at {swap_exe_path}")
        
        typer.echo(f"  Platform: {system}")
        typer.echo(f"  Package location: {info['package_location']}")
        
        if not swap_available:
            typer.echo("")
            typer.echo("To install SWAP, run: pyswap get-swap")
    
    return info

def get_swap(
    version: str = "4.2.0",
    force: bool = False,
    verbose: bool = True,
) -> str:
    """Download and setup SWAP executable for the current platform.
    
    Args:
        version: SWAP version to download. Defaults to "4.2.0".
        force: Force re-download even if executable already exists. Defaults to False.
        verbose: Print download progress and information. Defaults to True.
        
    Returns:
        Path to the SWAP executable.
        
    Examples:
        >>> import pyswap as psp
        >>> swap_exe = psp.get_swap()
        >>> print(f"SWAP executable available at: {swap_exe}")
        
        >>> # Force re-download latest version
        >>> swap_exe = psp.get_swap(force=True, verbose=True)
    """

    exe_path = get_swap_executable_path()
    
    # Check if executable already exists
    if os.path.exists(exe_path) and not force:
        if verbose:
            typer.echo(f"SWAP executable already exists at: {exe_path}")
            typer.echo("Use force=True to re-download")
        return exe_path
    
    # Download and install
    if verbose:
        typer.echo(f"Downloading SWAP {version} for {"windows" if IS_WINDOWS else "linux"}...")
        typer.echo(f"Installing to: {exe_path.parent}")
    
    try:
        _download_swap_executable(
            version=version,
            target_path=exe_path,
            verbose=verbose
        )
        
        write_version_info(version)
        if verbose:
            typer.echo(f"✓ SWAP {version} successfully installed!")
            typer.echo(f"Executable path: {exe_path}")
            typer.echo("Updated version info file.")
        return exe_path
        
    except Exception as e:
        raise typer.Exit(f"Failed to download SWAP executable: {e}")


def _download_swap_executable(
    version: str,
    target_path: str,
    verbose: bool = True
) -> None:
    """Download and extract SWAP executable from GitHub releases."""
    
    # Construct download URL
    base_url = "https://github.com/SWAP-model/SWAP/releases/download"
    filename = f"swap{version}-{"windows" if IS_WINDOWS else "linux"}"
    if IS_WINDOWS:
        filename += ".exe"
        
    url = f"{base_url}/v{version}/{filename}"
    
    if verbose:
        typer.echo(f"Downloading from: {url}")
    
    try:
        # Download with progress
        if verbose:
            with typer.progressbar(length=100, label="Downloading") as progress:
                def progress_hook(block_num, block_size, total_size):
                    downloaded = block_num * block_size
                    if total_size > 0:
                        percent = min(100, (downloaded * 100) // total_size)
                        progress.update(1 if percent > progress.pos else 0)
                
                urllib.request.urlretrieve(url, target_path, progress_hook)
        else:
            urllib.request.urlretrieve(url, target_path)
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise RuntimeError(
                f"SWAP version {version} not found for platform {"windows" if IS_WINDOWS else "linux"}. "
                f"Check available releases at: https://github.com/SWAP-model/SWAP/releases"
            )
        else:
            raise RuntimeError(f"Download failed: HTTP {e.code}")
    except Exception as e:
        raise RuntimeError(f"Download failed: {e}")
    
    # Make executable (Unix systems)
    if not IS_WINDOWS:
        os.chmod(target_path, 0o755)


def check_swap(exe_path: Optional[str] = None, verbose: bool = True) -> bool:
    """Check if SWAP executable is available and working.
    
    Args:
        exe_path: Path to SWAP executable. If None, uses default package location.
        verbose: Print information about the check. Defaults to True.
        
    Returns:
        True if SWAP is available and working.
    """
    if exe_path is None:
        exe_path = get_swap_executable_path()
    
    if not os.path.exists(exe_path):
        if verbose:
            typer.echo(f"SWAP executable not found at: {exe_path}")
            typer.echo("Run get_swap() to download and install SWAP")
        return False
    
    # Try to run SWAP to check if it works
    try:
        result = subprocess.run(
            [exe_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            if verbose:
                typer.echo(f"✓ SWAP executable working: {exe_path}")
                if result.stdout.strip():
                    typer.echo(f"Version info: {result.stdout.strip()}")
            return True
        else:
            # Some SWAP executables might not support --version, try running without args
            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                timeout=5,
                input="\n"  # Provide empty input to exit quickly
            )
            
            if verbose:
                typer.echo(f"✓ SWAP executable working: {exe_path}")
            return True
            
    except subprocess.TimeoutExpired:
        if verbose:
            typer.echo(f"✗ SWAP executable timed out: {exe_path}")
        return False
    except Exception as e:
        if verbose:
            typer.echo(f"✗ Error checking SWAP executable: {e}")
        return False


def remove_swap(verbose: bool = True) -> bool:
    """Remove the SWAP executable from the package directory.
    
    Args:
        verbose: Print information about the removal. Defaults to True.
        
    Returns:
        True if removal was successful.
    """
    exe_path = get_swap_executable_path()
    
    if not os.path.exists(exe_path):
        if verbose:
            typer.echo("SWAP executable not found, nothing to remove")
        return True
    
    try:
        os.remove(exe_path)
        os.remove(exe_path.parent / "version.yaml")
        if verbose:
            typer.echo(f"✓ SWAP executable removed from: {exe_path}")
            typer.echo(f"✓ version.yaml removed from: {exe_path.parent / 'version.yaml'}")
        return True
    except Exception as e:
        if verbose:
            typer.echo(f"✗ Failed to remove SWAP executable: {e}")
        return False