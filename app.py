from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from setting import config


def create_app() -> Flask:
    from views.auth import router as auth_router
    from views.blog import router as blog_router
    from views.profile import router as profile_router
    
    app = Flask(__name__, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY
    )


    auth_router.install(app)
    blog_router.install(app)
    profile_router.install(app)

    return app