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
            "transfer_data = app.commands.dump_db:transfer_data",
            "from-json = app.commands.dir_from_json:dir_to_json",
            "to-json = app.commands.json_to_dir:json_to_dir",
            "list-json = app.commands.list_saved_dirs:saved_directories",
            "edit-json = app.commands.edit_ignore:edit_ignore"
        ],
    },
    include_package_data=True,
)
