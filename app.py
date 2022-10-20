from distutils.debug import DEBUG
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from setting import config


def create_app() -> Flask:
    from components.auth import router as auth_router
    from components.blog import router as blog_router
    
    app = Flask(__name__, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY=config.secret_key
    )


    auth_router.install(app)
    blog_router.install(app)

    return app