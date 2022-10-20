from calendar import c
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Config:
    secret_key = b'blablabla'
    pathfile = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_MIGRATE_REPO = os.path.join(pathfile, 'db_repository')
    @property
    def db_url(self):
        return f'sqlite:///{self.pathfile}/instance/flask.db'


config = Config()

engine = create_engine(config.db_url)
db_session = sessionmaker(bind=engine)()
Base = declarative_base()