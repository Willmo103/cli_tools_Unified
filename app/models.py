from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

class Global(Base):
    __tablename__ = "globals"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)

def init_db():
    Base.metadata.create_all(engine)

def get_globals():
    session = Session()
    globals_data = {g.key: g.value.split(",") for g in session.query(Global).all()}
    session.close()
    return globals_data

def update_globals(globals_data):
    session = Session()
    for key, value in globals_data.items():
        session.query(Global).filter(Global.key == key).update({"value": ",".join(value)})
    session.commit()
    session.close()
