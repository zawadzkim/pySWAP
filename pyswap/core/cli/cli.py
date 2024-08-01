"""The cli module is supposed to help in structuring the direcotries of created models and enforce
best practices in documenting. It creates a modular structure (with __init__.py files) what can be helpful when
writing scripts. This way, modules from the scripts can be directly imported into the main.py or main.ipynb"""

import json
import typer
import shutil
from pathlib import Path
import subprocess

app = typer.Typer()


def dict_to_custom_string(data):
    lines = [f"    {key}='{value}'," for key, value in data.items()]
    return "\n".join(lines)


def make_script(models_dir, basic_code_to_write_path, basic_code_to_write) -> str:

    main_script_path = models_dir / 'main.py'

    try:

        if not main_script_path.exists():
            main_script_path.touch()

        main_script_path.write_text(basic_code_to_write_path.read_text().format(
            formatted_string=basic_code_to_write))

        return print(f"Succesfully created main.py.")
    except Exception as e:
        return print(f"Error creating folder or file: {e}")


def make_notebook(models_dir, basic_code_to_write, templates_path, attrs) -> str:
    notebook_template_path = templates_path / 'notebook.json'
    notebook_path = models_dir / "main.ipynb"

    with open(notebook_template_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    try:

        notebook_content["cells"][0]["source"][0] = f"# {attrs['project']}\n"
        notebook_content["cells"][2]["source"][2] = basic_code_to_write

        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=4)

        print(f"Notebook {notebook_path} created successfully.")
    except Exception as e:
        print(f"Error creating Jupyter Notebook: {e}")


def copy_readme(templates_path, project_root):

    template_file = templates_path / 'README'
    shutil.copy(template_file, project_root)
    return 'Successfully created README in the root directory.'


def create_inits(project_root, models_dir, scripts_dir):
    (project_root / '__init__.py').touch()
    (models_dir / '__init__.py').touch()
    (scripts_dir / '__init__.py').touch()


def init_git_repo(project_root):
    try:
        subprocess.run(["git", "init", str(project_root)], check=True)
        print("Initialized empty Git repository.")

        # Create a .gitignore file
        gitignore_path = project_root / '.gitignore'
        with open(gitignore_path, 'w') as f:
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

        print(f"Created .gitignore file at {gitignore_path}")
    except Exception as e:
        print(f"Error initializing Git repository or creating .gitignore: {e}")


@app.command()
def init(script: bool = False, notebook: bool = True):
    """Prompt the user to enter their information and create a User class."""
    attrs = {
        'project': typer.prompt("Project name"),
        'swap_ver': typer.prompt("SWAP version used"),
        'author': typer.prompt("Author first/last name"),
        'institution': typer.prompt("Your last institution"),
        'email': typer.prompt("Your email address"),
        'comment': typer.prompt("Any comments?", default=None)
    }

    folder_name = typer.prompt(
        "Choose a folder name", default=attrs.get('project'))

    # Defining paths and creating folders.
    templates_path = Path(__file__).resolve().parent / 'templates'
    project_root = Path.cwd() / folder_name

    basic_code_to_write_path = templates_path / 'script.txt'
    basic_code_to_write = dict_to_custom_string(attrs)

    folders_to_create = ['models', 'scripts', 'data']
    folders_to_create_paths = [
        project_root / folder for folder in folders_to_create]

    [folder.mkdir(parents=True, exist_ok=True)
     for folder in folders_to_create_paths]

    # Dealing with files.
    copy_readme(templates_path, project_root)
    create_inits(project_root=project_root,
                 models_dir=folders_to_create_paths[0],
                 scripts_dir=folders_to_create_paths[1])

    if script:
        make_script(folders_to_create_paths[0],
                    basic_code_to_write_path, basic_code_to_write)

    if notebook:
        make_notebook(folders_to_create_paths[0],
                      basic_code_to_write, templates_path, attrs)

    init_git_repo(project_root)


@app.command()
def modify(script: bool = False, notebook: bool = True):
    print('Executing modify routine...')


if __name__ == "__main__":
    app()
