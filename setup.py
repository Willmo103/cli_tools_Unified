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
            "tojson = app.commands.dir_to_json:dir_to_json",
            "fmjson = app.commands.json_to_dir:json_to_dir",
            # "to-md = app.commands.dir_to_md:dir_to_md",
            "lsjson = app.commands.list_saved_dirs:list_saved_directories",
            "editjson = app.commands.edit_ignore:edit_ignore",
        ],
    },
    include_package_data=True,
)
