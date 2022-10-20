from curses import flash
from components.auth.decorator import login_required
from flask.views import MethodView
from flask import render_template, request
from components.user.model import User
from flask import redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

class LoginPage(MethodView):
    def get(self):
        return render_template('auth/login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.login(username)
        print(user.password)
        if user and check_password_hash(user.password, password): 
            session['login'] = user.username
            return redirect(url_for('index'))
        else: 
            return redirect(url_for('login'))


class RegisterPage(MethodView):
    def get(self):
        return render_template('auth/register.html')

    def post(self):
        username = request.form.get('username')
        password = request.form('password')
        if User.login(username) is not None:
            flash('Пользоваель существует')


class LogoutUser(MethodView):
    @login_required
    def get(self):
        session['login'] = None
        return redirect(url_for('login'))