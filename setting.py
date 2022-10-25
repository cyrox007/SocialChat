from calendar import c
import os

class Config:
    secret_key = b'blablabla'
    pathfile = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_MIGRATE_REPO = os.path.join(pathfile, 'db_repository')
    databaseUri = f'sqlite:///{pathfile}/instance/flask.db'


    FULL_AVATARS_PATH = pathfile+'/static/uploads/us_avatars/'
    AVATAR_DIR = 'uploads/us_avatars/'
    
    @property
    def db_url(self):
        return f'sqlite:///{self.pathfile}/instance/flask.db'


config = Config()