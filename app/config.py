from sqlalchemy import create_engine
from models import Log_Entry
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "cli_tools.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
TMP_LOG = os.path.join(BASE_DIR, "cli_tools.log")

db = create_engine(SQLALCHEMY_DATABASE_URI).connect()

log = logging.getLogger("toJson_logger")
log.FileHandler(TMP_LOG, mode="w", level=logging.DEBUG)
log.Formatter(
    "%(asctime)s:%(pathname)s:%(filename)s:%(lineno)s:%(levelname)s:%(message)s"  # noqa
)
log.setLevel(logging.DEBUG)


def log_to_database(level: str, message: str, name: str | None = None):
    if not name:
        name = "toJson_logger"
    try:
        try:
            _log = logging.getLogger(name)
            eval(f"_log.{level.lower()}(message)")
        except Exception as e:
            log.error(e)
        with open(TMP_LOG, "r") as f:
            for line in f:
                log_data = line.split(";")
                log_entry = Log_Entry(
                    logDate=log_data[0],
                    logPath=log_data[1],
                    logFileName=log_data[2],
                    logLineNo=log_data[3],
                    logLevel=log_data[4],
                    logMessage=log_data[5],
                )
        db.execute(log_entry)
        db.commit()
    except Exception as e:
        log.error(e)
    finally:
        db.close()
        os.remove(TMP_LOG)
