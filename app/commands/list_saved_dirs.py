import click
import json
import os
from app.models import Directory, Session


@click.command()
def list_saved_directories():
    session = Session()
    directories = session.query(Directory).all()
    session.close()

    if not directories:
        click.echo("No saved directories found.")
        return

    # List all saved directories
    click.echo("Saved directories:")
    for index, directory in enumerate(directories):
        click.echo(f"{index}: {directory.name}")

    # Let the user choose a directory
    selected_index = click.prompt(
        "Enter the index of the directory to generate JSON", type=int
    )

    if selected_index < 0 or selected_index >= len(directories):
        click.echo("Invalid selection.")
        return

    selected_directory = directories[selected_index]
    json_data = json.loads(selected_directory.json_data)
    output_file_name = f"{selected_directory.name}_repr.json"
    output_file_path = os.path.join(os.getcwd(), output_file_name)

    with open(output_file_path, "w") as f:
        json.dump(json_data, f, indent=4)

    click.echo(f"Generated JSON file saved to: {output_file_path}")
