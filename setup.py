from setuptools import setup, find_packages
import sqlite3
from config import DB_PATH

setup(
    name = "cli_tools",
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        'Click',
        'sqlalchemy',
    ],
    include_dirs=['commands', 'commands\dump_db.py'],
    entry_points = {
        'console_scripts': [
            'transfer_data = commands.dump_db:transfer_data',
            'dir_to_json = commands.dir_to_json:dir_to_json',
            'json_to_dir = commands.json_to_dir:json_to_dir',
        ],
    },
)



def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS globals (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE,
            value TEXT
        )
    """)

    default_ignored_files = [
        ".venv",
        "venv",
        ".gitignore",
        "__pycache__",
        "build",
        "dist",
        ".env",
        ".git",
        "*egg*",
        "*.json"
    ]

    c.execute("""
        INSERT OR IGNORE INTO globals (key, value)
        VALUES (?, ?)
    """, ("ignore", ",".join(default_ignored_files)))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
