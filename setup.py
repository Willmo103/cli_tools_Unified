from setuptools import setup, find_packages


setup(
    name="cli_tools",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Click",
        "sqlalchemy",
    ],
    entry_points={
        "console_scripts": [
            "to-json = app.commands.dir_to_json:dir_to_json",
            "from-json = app.commands.json_to_dir:json_to_dir",
            "list-json = app.commands.list_saved_dirs:list_saved_directories",
            "edit-json = app.commands.edit_ignore:edit_ignore",
        ],
    },
    include_package_data=True,
)
