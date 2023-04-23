from app.config import DB_PATH
from app.models import init_db, Global, Session


def initialize_db():
    init_db()
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
        "*.json",
    ]

    session = Session()
    if not session.query(Global).filter(Global.key == "ignore").first():
        new_global = Global(key="ignore", value=",".join(default_ignored_files))
        session.add(new_global)
        session.commit()

    session.close()


if __name__ == "__main__":
    initialize_db()
