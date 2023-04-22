import click
import os, json

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
@click.argument("json_obj", type=click.Path(exists=True))
@click.argument("path", type=click.Path())
def generate_directory(json_obj, path):
    """Generate directory structure based on JSON object"""
    with open(json_obj) as f:
        data = json.load(f)
    create_directory_structure(data, path)
    click.echo(f"Directory structure generated at {path}")

