import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "globals.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
