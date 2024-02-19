from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import SQLALCHEMY_DATABASE_URI

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


class Global(Base):
    __tablename__ = "globals"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)


class Directory(Base):
    __tablename__ = "directories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    json_data = Column(String, nullable=True)


class Log_Entry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True)
    logDate = Column(String, nullable=False)
    logPath = Column(String, nullable=False)
    logFileName = Column(String, nullable=False)
    logLineNo = Column(Integer, nullable=False)
    logLevel = Column(String, nullable=False)
    logMessage = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(engine)


def get_globals():
    session = Session()
    globals_data = {
        g.key: g.value.split(",") for g in session.query(Global).all()
    }  # noqa
    session.close()
    return globals_data


def update_globals(globals_data):
    session = Session()
    for key, value in globals_data.items():
        session.query(Global).filter(Global.key == key).update(
            {"value": ",".join(value)}
        )
    session.commit()
    session.close()


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
        "ini",
        "jpg",
        "zip",
        "pdf",
        "jar",
        "png",
        "exe",
        "ctb",
        "ctx",
        "ctx~",
        "ctx~~",
        "ctx~~~",
        "lnk",
        "pack",
        "ico",
        "wasm",
        "jekyll-metadata",
        "swf",
        "gif",
        "lock",
        "bin",
        "tar",
        "dll",
        "pyd",
        "lib",
        "*amd64",
        "mp4",
        "npz",
        "node_modules",
        ".vscode",
        "package-lock.json",
        "*.db",
    ]

    session = Session()
    if not session.query(Global).filter(Global.key == "ignore").first():
        new_global = Global(
            key="ignore", value=",".join(default_ignored_files)
        )
        session.add(new_global)
        session.commit()

    session.close()
