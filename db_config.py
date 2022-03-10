from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser

connection_string = 'postgresql+psycopg2://postgres:admin@localhost:5431/test_db'

config = ConfigParser()

Base = declarative_base()


def create_all_entities():
    Base.metadata.create_all(engine)

Session = sessionmaker()
engine = create_engine(connection_string, echo=True)
local_session = Session(bind=engine)


