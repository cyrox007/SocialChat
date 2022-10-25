import os
from flask import render_template, request, flash, redirect, url_for, session
from flask.views import MethodView

from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from components.auth.decorator import login_required
from components.user.model import Profile, User
from database import Database
from setting import config

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        db_session = Database.connect_database()
        
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first-name')
        surname = request.form.get('surname')
        age = request.form.get('age')
        avatar = request.files['avatar']
        
        if User.login(db_session, username) is not None:
            flash('Пользователь с таким логином уже зарегестрирован')
            return render_template('auth/register.html')
        
        if avatar.filename == '':
            avatarPath = 'uploads/us_avatars/user_default.jpg'
        else:
            filename = secure_filename(avatar.filename)
            avatarPath = config.AVATAR_DIR+filename
            avatar.save(os.path.join(config.FULL_AVATARS_PATH, filename))

        new_user = User.registering_new_user(
                db_session=db_session, 
                login=username, 
                password=password
            )
        
        getUser = User.login(db_session, new_user.username)
        update_profile = Profile.insert_profile(
            db_session=db_session,
            user_id=getUser.id,
            first_name=first_name,
            surname=surname,
            age=age,
            avatar=avatarPath
        )
        
        if new_user is not None:
            session['login'] = getUser.username
            return redirect(url_for('index'))

        


class LogoutUser(MethodView):
    @login_required
    def get(self):
        session.clear()
        return redirect(url_for('login'))