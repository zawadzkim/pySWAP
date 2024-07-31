import os
import typer
import pyswap as ps
from pathlib import Path

app = typer.Typer()


def dict_to_custom_string(data):
    lines = [f"    {key}='{value}'," for key, value in data.items()]
    return "\n".join(lines)


@app.command()
def init(script: bool = False, notebook: bool = True):
    """Prompt the user to enter their information and create a User class."""
    attrs = {
        'project': typer.prompt("Project name"),
        'swap_ver': typer.prompt("SWAP version used"),
        'author': typer.prompt("Author firt/last name"),
        'institution': typer.prompt("Your last institution"),
        'email': typer.prompt("Your email address"),
        'comment': typer.prompt("Any comments?", default=None)}

    folder_name = typer.prompt(
        "Choose a folder name", default=attrs.get('project'))

    templates_path = Path(__file__).resolve().parent / 'templates'

    try:
        models_path = Path.cwd() / folder_name / 'models' / 'main.py'
        data_path = Path.cwd() / folder_name / 'data'

        data_path.mkdir(parents=True, exist_ok=True)
        models_path.parent.mkdir(parents=True, exist_ok=True)

        if not models_path.exists():
            models_path.touch()

        text_to_write = templates_path / 'template.txt'

        formatted_string = dict_to_custom_string(attrs)
        models_path.write_text(text_to_write.read_text().format(
            formatted_string=formatted_string))

        print(
            f"Folder '{folder_name}' and file 'user.py' created successfully with the User class.")
    except Exception as e:
        print(f"Error creating folder or file{e}")


@app.command()
def modify():
    print("Executing modify routine...")


if __name__ == "__main__":
    app()
