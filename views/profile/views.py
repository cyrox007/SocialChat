from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request, flash
from database import Database
from components.user.model import User
from components.auth.decorator import login_required


class ProfilePage(MethodView):
    @login_required
    def get(self, login):
        return render_template(
            'profile/index.html'
        )