from sqlalchemy import Column, Integer, String
from setting import Base, db_session


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


    @classmethod
    def login(cls, login):
        user = db_session.query(User).filter(
            User.username == login
            ).first()
        db_session.close()
        return user


    @classmethod
    def get_user_id(cls, login):
        user_id = db_session.query(User.id).filter(
            User.username == login
            ).first()

        db_session.close()
        return user_id.id


