"""
SWAP executable management module.

This module provides functionality to download and manage SWAP executables
similar to how flopy handles MODFLOW executables.
"""

import os
import platform
import shutil
import subprocess
import urllib.request
from pathlib import Path

import typer
import yaml

import pyswap
from pyswap.core.defaults import IS_WINDOWS


def check_missing_dlls_windows(exe_path: str) -> list[str]:
    """Check for missing DLL dependencies on Windows.

    Uses dumpbin (if available) to list dependencies, then checks which are missing.

    Args:
        exe_path: Path to the executable to check.

    Returns:
        List of missing DLL names, or empty list if all found or cannot check.
    """
    if platform.system() != "Windows":
        return []

    missing = []

    # Try to use dumpbin (comes with Visual Studio)
    dumpbin = shutil.which("dumpbin")
    if dumpbin:
        try:
            result = subprocess.run(
                [dumpbin, "/dependents", exe_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            # Parse dumpbin output to find DLL names
            in_section = False
            for line in result.stdout.splitlines():
                if "Image has the following dependencies:" in line:
                    in_section = True
                    continue
                if in_section:
                    line = line.strip()
                    if line and line.endswith(".dll"):
                        # Check if DLL exists in PATH
                        if not shutil.which(line):
                            missing.append(line)
                    elif line == "Summary":
                        break
        except Exception:
            print("Warning: Could not run dumpbin to check DLL dependencies.")
            pass

    return missing


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


def read_swap_version() -> str | None:
    """Read the SWAP version from the version file."""
    version_file = get_swap_executable_path().parent / "version.yaml"
    if version_file.exists():
        try:
            with version_file.open("r") as f:
                data = yaml.safe_load(f)
                return data.get("version_swap")  # type: ignore[no-any-return]
        except Exception:
            return None
    return None


def show_info() -> dict:
    """Display information about pySWAP and SWAP versions and installation.

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
        "package_location": str(Path(pyswap.__file__).parent),
    }

    typer.echo("=" * 40)
    typer.echo("pySWAP Setup Information:")
    typer.echo(f"  pySWAP version: {pyswap_version}")
    if swap_version:
        version_label = (
            "custom/uploaded" if swap_version == "custom" else swap_version
        )
        typer.echo(f"  SWAP version: {version_label}")
    else:
        typer.echo("  SWAP version: Not installed")

    if swap_available:
        typer.echo(f"  SWAP executable: ✓ Available at {swap_exe_path}")
    else:
        typer.echo(f"  SWAP executable: ✗ Not found at {swap_exe_path}")

    typer.echo(f"  Platform: {system}")
    typer.echo(f"  Package location: {info['package_location']}")

    if not swap_available:
        typer.echo("")
        typer.echo("To install SWAP:")
        typer.echo("  - Download: pyswap get-swap")
        typer.echo("  - Upload local file: pyswap upload-swap <path-to-executable>")

    typer.echo("=" * 40)

    return info


def get_swap(
    version: str = "4.2.0",
    force: bool = False,
    verbose: bool = True,
    auto_install: bool = False,
) -> str:
    """Download and setup SWAP executable for the current platform.

    Args:
        version: SWAP version to download. Defaults to "4.2.0".
        force: Force re-download even if executable already exists. Defaults to False.
        verbose: Print download progress and information. Defaults to True.
        auto_install: Automatically install SWAP if not found during the model run. Defaults to False.
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
    if verbose or auto_install:
        platform_name = "windows" if IS_WINDOWS else "linux"
        typer.echo(f"Downloading SWAP {version} for {platform_name}...")
        typer.echo(f"Installing to: {exe_path.parent}")

    try:
        _download_swap_executable(
            version=version, target_path=exe_path, verbose=verbose or auto_install
        )

        write_version_info(version)
        if verbose or auto_install:
            typer.echo(f"✓ SWAP {version} successfully installed!")
            typer.echo(f"Executable path: {exe_path}")
            typer.echo("Updated version info file.")
    except Exception as e:
        msg = f"Failed to download SWAP executable: {e}"
        raise typer.Exit(msg) from e
    else:
        return exe_path


def _download_swap_executable(
    version: str, target_path: str, verbose: bool = True
) -> None:
    """Download and extract SWAP executable from GitHub releases."""

    # Construct download URL
    base_url = "https://github.com/SWAP-model/SWAP/releases/download"
    platform_name = "windows" if IS_WINDOWS else "linux"
    filename = f"swap{version}-{platform_name}"
    if IS_WINDOWS:
        filename += ".exe"

    url = f"{base_url}/v{version}/{filename}"

    if verbose:
        typer.echo(f"Downloading from: {url}")

    try:
        # Download with progress
        if verbose:
            with typer.progressbar(length=100, label="Downloading") as progress:  # type: ignore[var-annotated]

                def progress_hook(
                    block_num: int, block_size: int, total_size: int
                ) -> None:
                    downloaded = block_num * block_size
                    if total_size > 0:
                        percent = min(100, (downloaded * 100) // total_size)
                        progress.update(1 if percent > progress.pos else 0)

                urllib.request.urlretrieve(url, target_path, progress_hook)
        else:
            urllib.request.urlretrieve(url, target_path)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            platform_name = "windows" if IS_WINDOWS else "linux"
            msg = (
                f"SWAP version {version} not found for platform {platform_name}. "
                f"Check available releases at: https://github.com/SWAP-model/SWAP/releases"
            )
            raise RuntimeError(msg) from e
        else:
            msg = f"Download failed: HTTP {e.code}"
            raise RuntimeError(msg) from e
    except Exception as e:
        msg = f"Download failed: {e}"
        raise RuntimeError(msg) from e

    # Make executable (Unix systems)
    if not IS_WINDOWS:
        os.chmod(target_path, 0o755)


def check_swap(exe_path: str | None = None, verbose: bool = True) -> bool:
    """Check if SWAP executable is available and working by running a testcase.

    Args:
        exe_path: Path to SWAP executable. If None, uses default package location.
        verbose: Print information about the check. Defaults to True.

    Returns:
        True if SWAP is available and working.
    """
    if exe_path is None:
        exe_path = str(get_swap_executable_path())

    if not os.path.exists(exe_path):
        if verbose:
            typer.echo(f"SWAP executable not found at: {exe_path}")
            typer.echo("Run get_swap() to download and install SWAP")
        return False

    # Check for missing DLLs on Windows before running testcase
    if IS_WINDOWS and verbose:
        missing_dlls = check_missing_dlls_windows(exe_path)
        if missing_dlls:
            typer.echo(f"⚠ Warning: Missing DLL dependencies detected: {', '.join(missing_dlls)}")
            typer.echo("This will likely cause the executable to fail.")
            typer.echo("\nRecommended solutions:")
            typer.echo("  1. Install Microsoft Visual C++ Redistributable:")
            typer.echo("     https://aka.ms/vs/17/release/vc_redist.x64.exe")
            typer.echo("  2. Or try an older SWAP version: pyswap get-swap --version 4.1.0")
            typer.echo("")

    # Try to run SWAP by executing a simple testcase
    try:
        from pyswap import testcase

        if verbose:
            show_info()
            typer.echo(f"Running testcase to verify SWAP executable: {exe_path}")
            typer.echo("Loading hupselbrook testcase...")

        # Get the testcase and run it
        hupselbrook = testcase.get("hupselbrook")
        result = hupselbrook.run()
        print(result)

        if verbose:
            typer.echo("✓ SWAP testcase completed successfully!")
            typer.echo(f"✓ SWAP executable working: {exe_path}")
            # Show a brief summary
            yearly_data = result.yearly_summary
            if not yearly_data.empty:
                total_years = len(yearly_data)
                avg_rain = yearly_data['RAIN'].mean()
                avg_drainage = yearly_data['DRAINAGE'].mean()
                typer.echo(f"Testcase summary: {total_years} years, avg rainfall: {avg_rain:.1f}mm, avg drainage: {avg_drainage:.1f}mm")

    except Exception as e:
        if verbose:
            typer.echo(f"✗ Error running SWAP testcase: {e}")
            typer.echo("This could indicate a problem with the SWAP executable or installation")
        return False
    else:
        return True
def upload_swap(
    file_path: str,
    version: str,
    force: bool = False,
    verbose: bool = True,
) -> str:
    """Install SWAP executable from a local file.

    Args:
        file_path: Path to the local SWAP executable file to install.
        version: Version identifier for the uploaded executable. Defaults to "custom".
        force: Force replace existing executable. Defaults to False.
        verbose: Print installation progress and information. Defaults to True.

    Returns:
        Path to the installed SWAP executable.

    Examples:
        >>> import pyswap as psp
        >>> # Install from a local executable
        >>> swap_exe = psp.upload_swap("/path/to/my/swap", version="4.2.1-custom")
        >>> print(f"SWAP executable installed at: {swap_exe}")

        >>> # Force replace existing installation
        >>> swap_exe = psp.upload_swap("./swap420", force=True, verbose=True)
    """
    from pathlib import Path

    source_path = Path(file_path)
    target_path = get_swap_executable_path()

    # Validate source file
    if not source_path.exists():
        msg = f"Source file not found: {source_path}"
        raise FileNotFoundError(msg)

    if not source_path.is_file():
        msg = f"Source path is not a file: {source_path}"
        raise ValueError(msg)

    # Check if target already exists
    if target_path.exists() and not force:
        current_version = read_swap_version()
        msg = (
            f"SWAP executable already exists at: {target_path}\n"
            f"Current version: {current_version or 'unknown'}\n"
            f"Use force=True to replace it."
        )
        raise FileExistsError(msg)

    if verbose:
        typer.echo(f"Installing SWAP executable from: {source_path}")
        typer.echo(f"Target location: {target_path}")
        if target_path.exists():
            typer.echo("Replacing existing executable...")

    try:
        # Create target directory if it doesn't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(source_path, target_path)

        # Make executable (Unix systems)
        if not IS_WINDOWS:
            os.chmod(target_path, 0o755)

        # Verify the copied file
        if not _verify_executable(target_path, verbose=verbose):
            # Clean up on failure
            target_path.unlink(missing_ok=True)
            msg = "Uploaded file does not appear to be a valid executable"
            raise RuntimeError(msg)

        # Write version info
        write_version_info(version)

        if verbose:
            typer.echo("✓ Your SWAP executable successfully installed!")
            typer.echo(f"Version: {version}")
            typer.echo(f"Executable path: {target_path}")

        return str(target_path)

    except Exception as e:
        if verbose:
            typer.echo(f"✗ Failed to install SWAP executable: {e}")
        raise


def _verify_executable(exe_path: Path, verbose: bool = False) -> bool:
    """Verify that the uploaded file is a valid executable.

    This could be expanded if we could make sure there --version always works on swap.
    For now it seems it spits out the version output to a file instead of just stdout.

    Args:
        exe_path: Path to the executable to verify.
        verbose: Print verification details.

    Returns:
        True if the file appears to be a valid executable.
    """
    try:
        # Check if file is executable
        if not os.access(exe_path, os.X_OK):
            if verbose:
                typer.echo("File is not executable")
            return False

        typer.echo("Warning: Uploading unverified executable.")

    except subprocess.TimeoutExpired:
        if verbose:
            typer.echo("Warning: Executable test timed out, but installing anyway")
        return True
    except Exception as e:
        if verbose:
            typer.echo(
                f"Warning: Could not verify executable ({e}), but installing anyway"
            )
        return True
    else:
        return True


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
            typer.echo(
                f"✓ version.yaml removed from: {exe_path.parent / 'version.yaml'}"
            )
    except Exception as e:
        if verbose:
            typer.echo(f"✗ Failed to remove SWAP executable: {e}")
        return False
    else:
        return True
