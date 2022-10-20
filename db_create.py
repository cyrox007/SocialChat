#!flask/bin/python
from migrate.versioning import api
from setting import config, Base, engine
import os


Base.metadata.create_all(engine)
if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
    api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(config.db_url, config.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(
        config.db_url, 
        config.SQLALCHEMY_MIGRATE_REPO, 
        api.version(config.SQLALCHEMY_MIGRATE_REPO)
        )