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
            "dir_to_json = app.commands.dir_to_json:dir_to_json",
            "json_to_dir = app.commands.json_to_dir:json_to_dir",
            "generate_json = app.commands.generate_json:generate_json",
        ],
    },
    include_package_data=True,
)
