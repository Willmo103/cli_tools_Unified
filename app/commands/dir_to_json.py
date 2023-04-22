import click
import os, json, fnmatch
from models import get_globals, update_globals, Session, Global, Directory


def remove_pwd(path):
    pwd = os.path.normpath(os.getcwd())
    if path.startswith(pwd):
        stripped_path = path[len(pwd) + 1 :]
        return stripped_path
    else:
        return path


@click.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Creates full file structure adding empty dicts for all directories present and empty str for all files present",
)
@click.argument("dir_path", type=click.Path(exists=True))
def dir_to_json(dir_path, all):
    """"""
    # Get the directory name from the dir_path argument
    directory_name = os.path.basename(os.path.abspath(dir_path))

    # remove the pwd from the path to avoid extra nesting
    dir_path = remove_pwd(os.path.normpath(dir_path))

    # Use the directory name to construct the output file name
    output_file_name = directory_name + "_repr.json"

    globals_data = get_globals()
    ignored_files = globals_data["ignore"]

    # Create an empty dictionary to store the file tree
    file_tree = {}

    # Traverse the directory and get the file tree
    for root, dirs, files in os.walk(dir_path):
        # print(root, "\n\n")
        current_dir = file_tree
        # Traverse all the directories in the current directory
        for directory in os.path.normpath(root).split(os.path.sep):
            ignore_dir = False
            for pattern in ignored_files:
                if fnmatch.fnmatch(directory, pattern):
                    ignore_dir = True
            if ignore_dir:
                if all:
                    current_dir = current_dir.setdefault(
                        os.path.basename(os.path.abspath(directory)), {}
                    )
                break
            current_dir = current_dir.setdefault(
                os.path.basename(os.path.abspath(directory)), {}
            )
        else:
            # Traverse all the files in the current directory
            for filename in files:
                # Check if the file matches the ignored_files patterns
                ignore_file = False
                for pattern in ignored_files:
                    if fnmatch.fnmatch(filename, pattern):
                        ignore_file = True
                        break
                if ignore_file:
                    if all:
                        current_dir[filename] = ""
                    continue

                # Get the full path of the file
                filepath = os.path.join(root, filename)

                # Read the contents of the file
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        file_contents = f.read()
                except Exception as e:
                    print(os.path.basename(filepath).split(".")[1])
                    print(e)
                    continue
                # Add the file contents to the file tree
                current_dir[filename] = file_contents

    # Use the current working directory instead of the module's path
    output_file_path = os.path.join(os.getcwd(), output_file_name)
    session = Session()
    new_directory = Directory(name=directory_name, json_data=json.dumps(file_tree))
    session.add(new_directory)
    session.commit()
    session.close()

    with open(output_file_path, "w") as f:
        json.dump(file_tree, f, indent=4)

    return


@click.command()
@click.option("-a", "--add", is_flag=True, help="Add a file to the ignore list")
@click.option("-d", "--delete", is_flag=True, help="Delete a file from the ignore list")
@click.option(
    "-l", "--list", "list_", is_flag=True, help="List all files in the ignore list"
)
def code_edit_ignore(add, delete, list_):
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
