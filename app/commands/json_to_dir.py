import click
import os, json
from . import Directory, Session


def create_directory_structure(data, path):
    """Create directory structure based on JSON object"""
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = os.path.join(path, str(key))
            if isinstance(value, str):
                with open(new_path, "w") as f:
                    f.write(value)
            else:
                os.makedirs(new_path, exist_ok=True)
                create_directory_structure(value, new_path)


@click.command()
@click.argument("json_obj", type=click.Path(exists=True), required=False)
@click.argument("path", type=click.Path())
def json_to_dir(json_obj, path):
    session = Session()
    directories = session.query(Directory).all()
    session.close()

    if directories:
        # List all saved directories
        click.echo("Saved directories:")
        for index, directory in enumerate(directories):
            click.echo(f"{index}: {directory.name}")

        # Let the user choose a directory
        selected_index = click.prompt(
            "Enter the index of the directory to generate", type=int
        )

        if selected_index < 0 or selected_index >= len(directories):
            click.echo("Invalid selection.")
            return

        selected_directory = directories[selected_index]
        data = json.loads(selected_directory.json_data)

    elif json_obj:
        with open(json_obj) as f:
            data = json.load(f)

    else:
        # Prompt the user to enter a JSON file path
        json_file_path = click.prompt(
            "Enter the path to a JSON file", type=click.Path(exists=True)
        )
        with open(json_file_path) as f:
            data = json.load(f)

    create_directory_structure(data, path)
    click.echo(f"Directory structure generated at {path}")
