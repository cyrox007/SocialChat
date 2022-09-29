from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.get('/')
def index():
    title = "Блог"
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
def create():
    return render_template(
        'home/create.html'
    )