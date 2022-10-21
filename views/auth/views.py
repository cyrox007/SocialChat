from flask import render_template, request, flash, redirect, url_for, session
from flask.views import MethodView

from werkzeug.security import check_password_hash

from components.auth.decorator import login_required
from components.user.model import User
from database import Database


class LoginPage(MethodView):
    def get(self):
        return render_template('auth/login.html')

    def post(self):
        db_session = Database.connect_database()
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.login(db_session, username)
        db_session.close()
        if user is not None and check_password_hash(user.password, password): 
            session['login'] = user.username
            db_session.close()
            return redirect(url_for('index'))
        
        flash('Пользователя не существует')
        return redirect(url_for('login'))


class RegisterPage(MethodView):
    def get(self):
        return render_template('auth/register.html')

    def post(self):
        db_session = Database.connect_database()
        username = request.form.get('username')
        password = request.form.get('password')
        if User.login(db_session, username) is not None:
            flash('Пользователь с таким логином уже зарегестрирован')
            return render_template('auth/register.html')
        
        new_user = User.registering_new_user(
            db_session=db_session, 
            login=username, 
            password=password
            )
        if new_user is not None:
            session['login'] = new_user.username
            return redirect(url_for('index'))

        


class LogoutUser(MethodView):
    @login_required
    def get(self):
        session.clear()
        return redirect(url_for('login'))