""" ФАЙЛ СТАРЫЙ И НЕ АКТУЛЬНЫЙ, ОСТАВИЛ ПОТОМУ ЧТО НЕ ВСЕ ПЕРЕПИСАЛ В НОВУЮ СТРУКТУРУ """

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.get('/')
def index():
    title = "The matrix has you..."
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template(
            'home/index.html', 
            posts=posts, 
            title=title
        )


@bp.get('/create')
@login_required
def create():
    return render_template('home/create.html')

@bp.post('/create')
@login_required
def create_page():
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
        error = 'Название обязательно.'
    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (title, body, g.user['id'])
        )
        db.commit()
        return redirect(url_for('blog.index'))
    
    return render_template('home/create.html', error=error)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.get('/<int:id>/update')
@login_required
def update_page(id):
    return render_template(
        'blog/update.html', 
        post=get_post(id)
        )


@bp.post('/<int:id>/update')
@login_required
def update(id):
    title = request.form['title']
    body = request.form['body']
    error = None

    if not title:
        error = 'Title is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE post SET title = ?, body = ?'
            ' WHERE id = ?',
            (title, body, id)
        )
        db.commit()
        return redirect(url_for('blog.index'))


@bp.post('/<int:id>/delete')
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))