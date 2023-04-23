# Import your commands here to make them easily accessible when importing the 'commands' modules
from .config import SQLALCHEMY_DATABASE_URI, DB_PATH
from .models import (
    init_db as init_db,
    Global as Global,
    Session as Session,
    initialize_db as initialize_db,
    get_globals as get_globals,
    update_globals as update_globals,
    Directory as Directory,
)
import os

if not os.path.exists(DB_PATH):
    initialize_db()
