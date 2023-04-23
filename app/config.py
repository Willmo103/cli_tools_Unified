import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "cli_tools.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
