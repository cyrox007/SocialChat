from email.policy import default
from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from werkzeug.security import generate_password_hash

from database import Database

class User(Database.Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


    @classmethod
    def login(cls, db_session, login):
        user = db_session.query(User).filter(
            User.username == login
            ).first()
        return user


    @classmethod
    def registering_new_user(cls, db_session, login, password):
        new_user = User(
            username=login,
            password=generate_password_hash(password=password)
        )
        db_session.add(new_user)
        db_session.commit()
        return new_user


class Profile(Database.Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    first_name = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
    age = Column(DATE, nullable=True)
    avatar = Column(String, default='default_img.webp')