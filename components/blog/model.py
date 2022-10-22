from components.user.model import User
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from database import Database
from datetime import datetime

class Posts(Database.Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    created = Column(DateTime(), default=datetime.now)
    title = Column(String(50), nullable=False)
    body = Column(Text, nullable=False)

    @classmethod
    def get_posts(cls, db_session):
        posts = db_session.query(
            Posts.id, 
            Posts.author_id, 
            Posts.created, 
            Posts.title,
            Posts.body,
            User.username
            ).join(User).all()
        return posts

    @classmethod
    def get_user_posts(cls, db_session, user_id):
        posts = db_session.query(
            Posts.id, 
            Posts.author_id, 
            Posts.created, 
            Posts.title,
            Posts.body,
            User.username
            ).filter(
                Posts.author_id == user_id
            ).join(User).all()
        return posts

    def insert_new_post(db_session, title, text, author):
        post = Posts(
            author_id=author,
            title=title,
            body=text 
        )
        db_session.add(post)
        db_session.commit()

    def get_post(db_session, id):
        post = db_session.query(
            Posts.id,
            Posts.author_id, 
            Posts.created, 
            Posts.title,
            Posts.body
        ).filter(
            Posts.id == id
        ).first()
        return post

    def update_post(db_session, id, title, text):
        datapost = db_session.query(Posts).filter(Posts.id == id).first()
        datapost.title = title
        datapost.body = text
        db_session.add(datapost)
        db_session.commit()

    def delete_post(db_session, id):
        datapost = db_session.query(Posts).filter(Posts.id == id).first()
        db_session.delete(datapost)
        db_session.commit()
