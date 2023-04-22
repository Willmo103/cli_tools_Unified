import click
import os, json, fnmatch
from models import get_globals,  Session, Directory


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

