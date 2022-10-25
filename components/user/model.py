import os
from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from setting import config

from database import Database

class User(Database.Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"User {self.username}"


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
    avatar = Column(String, default='uploads/us_avatars/user_default.jpg')

    @classmethod
    def get_profile(cls, db_session, user_id):
        user = db_session.query(Profile).filter(
            Profile.user_id == user_id
        ).first()
        return user

    @classmethod
    def insert_profile(cls, db_session, user_id, first_name, surname, age, avatar):
        profile = Profile(
            user_id=user_id,
            first_name=first_name,
            surname=surname,
            age=datetime.strptime(age, "%Y-%m-%d").date(),
            avatar=avatar
        )
        db_session.add(profile)
        db_session.commit()

    
    @classmethod
    def update_profile(cls, db_session, user_id, first_name, surname, age, avatar):
        profile = Profile.get_profile(db_session, user_id)
        profile.first_name = first_name
        profile.surname = surname
        profile.age = datetime.strptime(age, "%Y-%m-%d").date()
        if avatar.filename == '':
            profile.avatar = profile.avatar
        else:
            old_avatar = profile.avatar
            filename = secure_filename(avatar.filename)
            profile.avatar = config.AVATAR_DIR+filename
            avatar.save(os.path.join(config.FULL_AVATARS_PATH, filename))
            old_avatar = old_avatar.split('/')
            old_avatar = old_avatar[-1]
            os.remove(os.path.join(config.FULL_AVATARS_PATH, old_avatar))

        db_session.add(profile)
        db_session.commit()
            


class UserToSubscriptions(Database.Base):
    __tablename__ = 'user_to_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    author_id = Column(Integer, ForeignKey('user.id'))

    