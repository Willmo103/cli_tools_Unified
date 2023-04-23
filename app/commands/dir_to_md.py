import click
import os, json, fnmatch
from . import get_globals, Session, Directory


def remove_pwd(path):
    pwd = os.path.normpath(os.getcwd())
    if path.startswith(pwd):
        stripped_path = path[len(pwd) + 1 :]
        return stripped_path
    else:
        return path


def build_tree_representation(current_dir, indent):
    tree_repr = ""
    for name, value in current_dir.items():
        if isinstance(value, dict):
            tree_repr += indent + "├── " + name + "\n"
            tree_repr += build_tree_representation(value, indent + "│   ")
        else:
            tree_repr += indent + "└── " + name + "\n"
    return tree_repr


@click.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="Creates full file structure adding empty dicts for all directories present and empty str for all files present",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Outputs a JSON with empty objects or strings representing the sample output structure of this command",
)
@click.argument("dir_path", type=click.Path(exists=True))
def dir_to_md(dir_path, all, debug):
    directory_name = os.path.basename(os.path.abspath(dir_path))
    dir_path = remove_pwd(os.path.normpath(dir_path))

    output_file_name = directory_name + "_repr.md"

    globals_data = get_globals()
    ignored_files = globals_data["ignore"]

    root_fp = os.path.basename(os.path.abspath(dir_path))
    file_tree = {f"{root_fp}": {}}

    for root, dirs, files in os.walk(dir_path):
        current_dir = file_tree[root_fp]

        dir_parts = os.path.normpath(root).split(os.path.sep)[1:]

        inside_ignored_dir = False

        for directory in dir_parts:
            ignore_dir = False
            for pattern in ignored_files:
                if fnmatch.fnmatch(directory, pattern):
                    ignore_dir = True
                elif directory.startswith(".git"):
                    ignore_dir = True
                    break
            if ignore_dir:
                inside_ignored_dir = True
                if all:
                    current_dir = current_dir.setdefault(directory, {})
                break
            current_dir = current_dir.setdefault(directory, {})

        if inside_ignored_dir:
            continue

        for filename in files:
            ignore_file = False
            for pattern in ignored_files:
                if fnmatch.fnmatch(filename, pattern):
                    ignore_file = True
                    break
            if ignore_file:
                if all:
                    current_dir[filename] = ""
                continue

            filepath = os.path.join(root, filename)

            if not debug:
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        file_contents = f.read()
                except Exception as e:
                    continue
            else:
                file_contents = ""

            current_dir[filename] = file_contents

    output_file_path = os.path.join(os.getcwd(), output_file_name)

    with open(output_file_path, "w") as f:
        tree_repr = build_tree_representation(file_tree, "")
        f.write(tree_repr)

    return
