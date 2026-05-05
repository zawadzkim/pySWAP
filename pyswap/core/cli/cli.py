# ruff: noqa: S607
# Those rules are not really useful in this package.

"""The cli module is supposed to help in structuring the direcotries of created models and enforce
best practices in documenting. It creates a modular structure (with __init__.py files) what can be helpful when
writing scripts. This way, modules from the scripts can be directly imported into the main.py or main.ipynb"""

import json
import shutil
import subprocess
from pathlib import Path

import typer

app = typer.Typer()


def dict_to_custom_string(data):
    lines = [f"    {key}='{value}'," for key, value in data.items()]
    return "\n".join(lines)


def make_script(models_dir, basic_code_to_write_path, basic_code_to_write) -> str:
    main_script_path = models_dir / "main.py"

    try:
        if not main_script_path.exists():
            main_script_path.touch()

        main_script_path.write_text(
            basic_code_to_write_path.read_text().format(
                formatted_string=basic_code_to_write
            )
        )

        return print("Succesfully created main.py.")
    except Exception as e:
        return print(f"Error creating folder or file: {e}")


def make_notebook(models_dir, basic_code_to_write, templates_path, attrs) -> None:
    notebook_template_path = templates_path / "notebook.json"
    notebook_path = models_dir / "main.ipynb"

    with open(notebook_template_path, encoding="utf-8") as f:
        notebook_content = json.load(f)
    try:
        notebook_content["cells"][0]["source"][0] = f"# {attrs['project']}\n"
        notebook_content["cells"][2]["source"][2] = basic_code_to_write

        with open(notebook_path, "w", encoding="utf-8") as f:
            json.dump(notebook_content, f, indent=4)

        print(f"Notebook {notebook_path} created successfully.")
    except Exception as e:
        print(f"Error creating Jupyter Notebook: {e}")

    return None


def copy_readme(templates_path, project_root, use_pixi=True, attrs=None):
    """Copy and customize README template based on whether pixi is used."""
    if use_pixi:
        template_file = templates_path / "README_template"
        pixi_instructions_file = templates_path / "pixi_instructions.md"

        readme_content = template_file.read_text()
        pixi_instructions = pixi_instructions_file.read_text()

        pixi_structure = "\n├── pixi.toml               # Pixi dependency management"

        readme_content = readme_content.format(
            project=attrs.get("project", "Project"),
            pixi_structure=pixi_structure,
            pixi_instructions=pixi_instructions
        )

        readme_path = project_root / "README.md"
        readme_path.write_text(readme_content)
    else:
        template_file = templates_path / "README"
        readme_content = template_file.read_text()

        readme_content = readme_content.format(
            project=attrs.get("project", "Project"),
            pixi_structure="",
            pixi_instructions=""
        )

        readme_path = project_root / "README"
        readme_path.write_text(readme_content)

    return "Successfully created README in the root directory."


def create_pixi_toml(templates_path, project_root, attrs):
    """Create pixi.toml file from template."""
    template_file = templates_path / "pixi.toml"
    pixi_content = template_file.read_text()

    # Format the template with user attributes
    pixi_content = pixi_content.format(
        author=attrs.get("author", "Unknown"),
        email=attrs.get("email", "unknown@example.com"),
        project=attrs.get("project", "pyswap-project")
    )

    pixi_path = project_root / "pixi.toml"
    pixi_path.write_text(pixi_content)

    return "Successfully created pixi.toml file."


def copy_crop_parameter_yaml(templates_path, models_dir):
    template_file = templates_path / "crop_tables_template.yaml"
    shutil.copy(template_file, models_dir)
    return "Successfully created crop_tables_template.yaml in the models directory."


def create_inits(project_root, models_dir, scripts_dir):
    (project_root / "__init__.py").touch()
    (models_dir / "__init__.py").touch()
    (scripts_dir / "__init__.py").touch()


def init_git_repo(project_root, use_pixi=False):
    try:
        result = subprocess.run(
            ["git", "init", str(project_root)],
            shell=False,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout.strip())

        # Create a .gitignore file
        gitignore_path = project_root / ".gitignore"
        with open(gitignore_path, "w") as f:
            f.write("# Python\n")
            f.write("__pycache__/\n")
            f.write("*.pyc\n")
            f.write("*.pyo\n")
            f.write("*.pyd\n")
            f.write(".env\n")
            f.write("venv/\n")
            f.write("env/\n")
            f.write("*.env\n")
            f.write("*.ipynb_checkpoints/\n")
            f.write("data/\n")

            if use_pixi:
                f.write("\n# Pixi\n")
                f.write(".pixi/\n")
                f.write("pixi.lock\n")

        print(f"Created .gitignore file at {gitignore_path}")
    except Exception as e:
        print(f"Error initializing Git repository or creating .gitignore: {e}")


@app.command()
def init(
    script: bool = False,
    notebook: bool = True,
    pixi: bool = typer.Option(True, "--pixi/--no-pixi", help="Include Pixi configuration for dependency management (default: True)")
):
    """Prompt the user to enter their information and create a User class."""
    attrs = {
        "project": typer.prompt("Project name"),
        "swap_ver": typer.prompt("SWAP version used"),
        "author": typer.prompt("Author first/last name"),
        "institution": typer.prompt("Your last institution"),
        "email": typer.prompt("Your email address"),
        "comment": typer.prompt("Any comments?", default=""),
    }

    folder_name = typer.prompt("Choose a folder name", default=attrs.get("project"))

    # Defining paths and creating folders.
    templates_path = Path(__file__).resolve().parent / "templates"
    project_root = Path.cwd() / folder_name

    basic_code_to_write_path = templates_path / "script.txt"
    basic_code_to_write = dict_to_custom_string(attrs)

    folders_to_create = ["models", "scripts", "data", "tests"]
    folders_to_create_paths = [project_root / folder for folder in folders_to_create]

    [folder.mkdir(parents=True, exist_ok=True) for folder in folders_to_create_paths]

    # Dealing with files.
    copy_readme(templates_path, project_root, use_pixi=pixi, attrs=attrs)
    create_inits(
        project_root=project_root,
        models_dir=folders_to_create_paths[0],
        scripts_dir=folders_to_create_paths[1],
    )

    # Create pixi.toml if requested
    if pixi:
        create_pixi_toml(templates_path, project_root, attrs)
        print("Created pixi.toml for dependency management.")

    if script:
        make_script(
            folders_to_create_paths[0], basic_code_to_write_path, basic_code_to_write
        )

    if notebook:
        make_notebook(
            folders_to_create_paths[0], basic_code_to_write, templates_path, attrs
        )

    init_git_repo(project_root, use_pixi=pixi)


@app.command()
def modify(script: bool = False, notebook: bool = True):
    print("Executing modify routine...")


@app.command()
def get_swap(
    version: str = typer.Option(
        "4.2.0", "--version", "-v", help="SWAP version to download"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force re-download even if executable exists"
    ),
    verbose: bool = typer.Option(
        True, "--verbose/--quiet", help="Enable verbose output"
    ),
):
    """Download and install SWAP executable."""
    from pyswap.utils.executables import get_swap as _get_swap

    try:
        exe_path = _get_swap(version=version, force=force, verbose=verbose)
        if verbose:
            typer.echo(f"Success! SWAP executable ready at: {exe_path}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def upload_swap(
    file_path: str = typer.Argument(help="Path to the SWAP executable file to install"),
    version: str = typer.Argument(
        help="Version identifier for the uploaded executable"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force replace existing executable"
    ),
    verbose: bool = typer.Option(
        True, "--verbose/--quiet", help="Enable verbose output"
    ),
):
    """Install SWAP executable from a local file."""
    from pyswap.utils.executables import upload_swap as _upload_swap

    try:
        exe_path = _upload_swap(
            file_path=file_path, version=version, force=force, verbose=verbose
        )
        if verbose:
            typer.echo(f"Success! SWAP executable installed at: {exe_path}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e


@app.command()
def check_swap(
    verbose: bool = typer.Option(
        True, "--verbose/--quiet", help="Enable verbose output"
    ),
):
    """Check if SWAP executable is available and working."""
    from pyswap.utils.executables import check_swap as _check_swap

    if _check_swap(verbose=verbose):
        typer.echo("✓ SWAP is ready to use!")
    else:
        typer.echo(
            "✗ SWAP is not available. Run 'pyswap get-swap' to install.", err=True
        )
        raise typer.Exit(1)


@app.command()
def remove_swap(
    verbose: bool = typer.Option(
        True, "--verbose/--quiet", help="Enable verbose output"
    ),
):
    """Remove SWAP executable from package directory."""
    from pyswap.utils.executables import remove_swap as _remove_swap

    if _remove_swap(verbose=verbose):
        typer.echo("SWAP executable removed successfully")
    else:
        typer.echo("Failed to remove SWAP executable", err=True)
        raise typer.Exit(1)


@app.command()
def info():
    """Display information about pySWAP and SWAP setup."""
    from pyswap.utils.executables import show_info

    show_info()

if __name__ == "__main__":
    app()
