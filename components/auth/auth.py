""" ФАЙЛ СТАРЫЙ И НЕ АКТУЛЬНЫЙ, ОСТАВИЛ ПОТОМУ ЧТО НЕ ВСЕ ПЕРЕПИСАЛ В НОВУЮ СТРУКТУРУ """

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/register')
def register_page():
    return render_template('auth/register.html')

@bp.post('/register')
def register():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None

    if not username or not password:
        error = 'Username or password is required.'

    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return redirect(url_for("auth.login"))

    flash(error)


@bp.get('/login')
def login_page():
    return render_template('auth/login.html')


@bp.post('/login')
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None or not check_password_hash(user['password'], password):
        error = 'Incorrect username or password.'
        return render_template('auth/login.html', error=error)

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view