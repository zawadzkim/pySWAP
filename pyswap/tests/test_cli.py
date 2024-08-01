import pytest
from typer.testing import CliRunner
from pathlib import Path
import shutil
import json

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
        "TestProjectFolder"
    ])

    result = runner.invoke(app, ['init', '--script'], input=inputs)
    assert result.exit_code == 0

    main_script_path = folder_path / "models" / "main.py"
    assert main_script_path.exists(), "main.py was not created."

    with open(main_script_path, "r") as f:
        content = f.read()
        assert "metadata = ps.Metadata(" in content, "Content of main.py is incorrect."


def test_cli_init_notebook(setup_and_teardown):
    folder_path = setup_and_teardown

    inputs = "\n".join([
        "TestProject",
        "1.0",
        "John Doe",
        "XYZ University",
        "john.doe@example.com",
        "No comments",
        "TestProjectFolder"
    ])

    result = runner.invoke(app, ['init', '--notebook'], input=inputs)
    assert result.exit_code == 0

    notebook_path = folder_path / "models" / "main.ipynb"
    assert notebook_path.exists(), "main.ipynb was not created."

    with open(notebook_path, "r") as f:
        notebook_content = json.load(f)

        code_cell_source = notebook_content["cells"][2]["source"]
        full_code_content = "".join(code_cell_source)
        assert "metadata = ps.Metadata(" in full_code_content, "Content of main.ipynb is incorrect."


def test_git_initialization_and_gitignore(setup_and_teardown):
    folder_path = setup_and_teardown

    inputs = "\n".join([
        "TestProject",
        "1.0",
        "John Doe",
        "XYZ University",
        "john.doe@example.com",
        "No comments",
        "TestProjectFolder"
    ])

    result = runner.invoke(
        app, ['init', '--script', '--notebook'], input=inputs)
    assert result.exit_code == 0

    git_dir_path = folder_path / ".git"
    assert git_dir_path.exists() and git_dir_path.is_dir(
    ), ".git directory was not created, Git repo not initialized."

    gitignore_path = folder_path / ".gitignore"
    assert gitignore_path.exists(), ".gitignore file was not created."

    with open(gitignore_path, "r") as f:
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
            "data/"
        ]

        for pattern in expected_patterns:
            assert pattern in gitignore_content, f"Expected pattern '{pattern}' not found in .gitignore file."


if __name__ == "__main__":
    pytest.main()
