import json
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

# Replace with the actual name of your script file
from pyswap.core.cli.cli import app

runner = CliRunner()


@pytest.fixture(scope="function")
def setup_and_teardown():
    # Setup: Define the folder and ensure it's clean
    folder_name = "TestProjectFolder"
    folder_path = Path.cwd() / folder_name

    # Clean up any existing folder
    if folder_path.exists():
        shutil.rmtree(folder_path)

    yield folder_path

    # Teardown: Clean up after the test
    if folder_path.exists():
        shutil.rmtree(folder_path)


def test_cli_init_script(setup_and_teardown):
    folder_path = setup_and_teardown

    inputs = "\n".join([
        "TestProject",
        "1.0",
        "John Doe",
        "XYZ University",
        "john.doe@example.com",
        "No comments",
        "TestProjectFolder",
    ])

    result = runner.invoke(app, ["init", "--script"], input=inputs)
    assert result.exit_code == 0

    main_script_path = folder_path / "models" / "main.py"
    assert main_script_path.exists(), "main.py was not created."

    with open(main_script_path) as f:
        content = f.read()
        assert "metadata = psp.components.Metadata(" in content, (
            "Content of main.py is incorrect."
        )


def test_cli_init_notebook(setup_and_teardown):
    folder_path = setup_and_teardown

    inputs = "\n".join([
        "TestProject",
        "1.0",
        "John Doe",
        "XYZ University",
        "john.doe@example.com",
        "No comments",
        "TestProjectFolder",
    ])

    result = runner.invoke(app, ["init", "--notebook"], input=inputs)
    assert result.exit_code == 0

    notebook_path = folder_path / "models" / "main.ipynb"
    assert notebook_path.exists(), "main.ipynb was not created."

    with open(notebook_path) as f:
        notebook_content = json.load(f)

        code_cell_source = notebook_content["cells"][2]["source"]
        full_code_content = "".join(code_cell_source)
        assert "metadata = ps.Metadata(" in full_code_content, (
            "Content of main.ipynb is incorrect."
        )


def test_git_initialization_and_gitignore(setup_and_teardown):
    folder_path = setup_and_teardown

    inputs = "\n".join([
        "TestProject",
        "1.0",
        "John Doe",
        "XYZ University",
        "john.doe@example.com",
        "No comments",
        "TestProjectFolder",
    ])

    result = runner.invoke(app, ["init", "--script", "--notebook"], input=inputs)
    assert result.exit_code == 0

    git_dir_path = folder_path / ".git"
    assert git_dir_path.exists() and git_dir_path.is_dir(), (
        ".git directory was not created, Git repo not initialized."
    )

    gitignore_path = folder_path / ".gitignore"
    assert gitignore_path.exists(), ".gitignore file was not created."

    with open(gitignore_path) as f:
        gitignore_content = f.read()
        expected_patterns = [
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".env",
            "venv/",
            "env/",
            "*.env",
            "*.ipynb_checkpoints/",
            "data/",
        ]

        for pattern in expected_patterns:
            assert pattern in gitignore_content, (
                f"Expected pattern '{pattern}' not found in .gitignore file."
            )


def test_upload_swap_success(tmp_path, monkeypatch):
    """Uploading a local executable should copy it to the package location and write version info."""
    from pyswap.core.cli.cli import app
    import pyswap.utils.executables as exe_mod

    runner = CliRunner()

    # Create a fake source executable
    src = tmp_path / "my_swap"
    src.write_text("#!/bin/sh\necho SWAP")
    src.chmod(0o755)

    # Prepare a fake install location and monkeypatch the getter
    install_dir = tmp_path / "install"
    install_dir.mkdir()
    target_path = install_dir / ("swap.exe" if exe_mod.IS_WINDOWS else "swap420")

    monkeypatch.setattr(exe_mod, "get_swap_executable_path", lambda: target_path)

    result = runner.invoke(app, ["upload-swap", str(src), "4.2.0", "--force"])
    assert result.exit_code == 0, result.stdout + str(result.exception)

    # Check file copied
    assert target_path.exists(), "Uploaded executable was not copied to target location"

    # Check version file
    version_file = target_path.parent / "version.yaml"
    assert version_file.exists(), "version.yaml was not written"
    version_txt = version_file.read_text()
    assert "4.2.0" in version_txt


def test_upload_swap_source_missing(tmp_path, monkeypatch):
    """Uploading a non-existent source should return an error."""
    from pyswap.core.cli.cli import app
    import pyswap.utils.executables as exe_mod

    runner = CliRunner()

    missing = tmp_path / "does_not_exist"

    install_dir = tmp_path / "install2"
    install_dir.mkdir()
    target_path = install_dir / ("swap.exe" if exe_mod.IS_WINDOWS else "swap420")
    monkeypatch.setattr(exe_mod, "get_swap_executable_path", lambda: target_path)

    result = runner.invoke(app, ["upload-swap", str(missing), "custom"])
    assert result.exit_code != 0
    assert "Source file not found" in result.stdout or "Error" in result.stdout


def test_upload_swap_target_exists_without_force(tmp_path, monkeypatch):
    """If target exists and --force not provided, upload should fail."""
    from pyswap.core.cli.cli import app
    import pyswap.utils.executables as exe_mod

    runner = CliRunner()

    src = tmp_path / "my_swap2"
    src.write_text("#!/bin/sh\necho SWAP")
    src.chmod(0o755)

    install_dir = tmp_path / "install3"
    install_dir.mkdir()
    target_path = install_dir / ("swap.exe" if exe_mod.IS_WINDOWS else "swap420")
    # create existing target
    target_path.write_text("existing")
    target_path.chmod(0o755)

    monkeypatch.setattr(exe_mod, "get_swap_executable_path", lambda: target_path)

    result = runner.invoke(app, ["upload-swap", str(src), "custom"])
    assert result.exit_code != 0
    assert "already exists" in result.stdout or "Use force=True" in result.stdout or "Use --force" in result.stdout
