
import click
from app.models import get_globals, update_globals


@click.command()
@click.option("-a", "--add", is_flag=True, help="Add a file to the ignore list")
@click.option("-d", "--delete", is_flag=True, help="Delete a file from the ignore list")
@click.option(
    "-l", "--list", "list_", is_flag=True, help="List all files in the ignore list"
)
def edit_ignore(add, delete, list_):
    globals_data = get_globals()
    ignored_files = globals_data["ignore"]

    if list_:
        # List all the files in the ignore list
        for i, item in enumerate(ignored_files):
            print(f"{i}: {item}")

    elif add:
        # Prompt the user to enter a filename to add
        filename = click.prompt("Enter a filename to ignore")
        if filename in ignored_files:
            click.echo(f"{filename} is already in the ignore list.")
        else:
            # Confirm with the user before adding the file to the ignore list
            if click.confirm(f"Add {filename} to the ignore list?"):
                ignored_files.append(filename)
                # Update the globals
                update_globals({"ignore": ignored_files})

    elif delete:
        # Prompt the user to select a file to delete
        for i, item in enumerate(ignored_files):
            print(f"{i}: {item}")
        selection = click.prompt("Enter the number of the item to delete", type=int)

        if selection < 0 or selection >= len(ignored_files):
            click.echo(f"Invalid selection: {selection}")
        else:
            # Confirm with the user before deleting the file from the ignore list
            filename = ignored_files[selection]

            if click.confirm(f"Delete {filename} from the ignore list?"):
                ignored_files.pop(selection)
                # Update the globals
                update_globals({"ignore": ignored_files})

    else:
        # No options specified, so just list all files in the ignore list
        for i, item in enumerate(ignored_files):
            print(f"{i}: {item}")
