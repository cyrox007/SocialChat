from components.user.model import User
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from setting import Base, db_session
from datetime import datetime

class Posts(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    created = Column(DateTime(), default=datetime.now)
    title = Column(String(50), nullable=False)
    body = Column(Text, nullable=False)

    @classmethod
    def get_posts(cls, user_id):
        posts = db_session.query(
            Posts.id, 
            Posts.author_id, 
            Posts.created, 
            Posts.title,
            Posts.body,
            User.username
            ).join(User).all()
        db_session.close()
        return posts

    def insert_new_post(title, text, author):
        post = Posts(
            author_id=author,
            title=title,
            body=text 
        )
        db_session.add(post)
        db_session.commit()
        db_session.close()

    def get_post(id):
        post = db_session.query(
            Posts.id,
            Posts.author_id, 
            Posts.created, 
            Posts.title,
            Posts.body
        ).filter(
            Posts.id == id
        ).first()
        db_session.close()
        return post

    def update_post(id, title, text):
        datapost = db_session.query(Posts).filter(Posts.id == id).first()
        datapost.title = title
        datapost.body = text
        db_session.add(datapost)
        db_session.commit()
        db_session.close()

    def delete_post(id):
        datapost = db_session.query(Posts).filter(Posts.id == id).first()
        db_session.delete(datapost)
        db_session.commit()
        db_session.close()
