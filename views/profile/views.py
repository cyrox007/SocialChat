from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request, flash
from database import Database
from components.user.model import User, Profile
from components.blog.model import Posts
from components.auth.decorator import login_required

from datetime import datetime


class ProfilePage(MethodView):
    @login_required
    def get(self, login):
        db_session = Database.connect_database()

        if session.get('login') != login:
            user = User.login(db_session, session.get('login'))
            otherUser = User.login(db_session, login)
            profile = Profile.get_profile(db_session, otherUser.id)
            posts = Posts.get_user_posts(db_session, otherUser.id)
        else:
            user = User.login(db_session, login)
            profile = Profile.get_profile(db_session, user.id)
            posts = Posts.get_user_posts(db_session, user.id)

        db_session.close()
        return render_template(
            'profile/index.html',
            user_id=user.id,
            login=login,
            profile=profile,
            posts=posts
        )


class SubstractAuthor(MethodView):
    @login_required
    def post(self, login):
        pass