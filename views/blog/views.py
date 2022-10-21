from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request, flash
from database import Database
from components.auth.decorator import login_required
from components.user.model import User
from components.blog.model import Posts


class MainPage(MethodView):
    @login_required
    def get(self):
        db_session = Database.connect_database()
        user = User.login(db_session, session.get('login'))
        posts = Posts.get_posts(db_session, user.id)
        db_session.close()
        return render_template(
            'home/index.html', 
            user_id=user.id, 
            posts=posts
            )


class CreatePost(MethodView):
    @login_required
    def get(self):
        return render_template('home/create.html')

    @login_required
    def post(self):
        db_session = Database.connect_database()
        user = User.login(db_session, session.get('login'))
        
        title = request.form.get('title')
        body = request.form.get('body')
        
        if title is None or body is None:
            flash("Заголовок и текст не могут быть пустыми")
        
        Posts.insert_new_post(db_session, title, body, user.id)
        db_session.close()
        return redirect(url_for('index'))


class UpdatePost(MethodView):
    @login_required
    def get(self, id):
        db_session = Database.connect_database()
        user = User.login(db_session, session.get('login'))

        post = Posts.get_post(db_session, id=id)
        if user.id != post.author_id:
            return redirect(url_for('404'), 404)
        
        db_session.close()
        return render_template('blog/update.html', post=post)

    def post(self, id):
        db_session = Database.connect_database()
        
        title = request.form.get('title')
        body = request.form.get('body')
        
        Posts.update_post(db_session, id, title, body)

        db_session.close()
        return redirect(url_for('index'))


class DeletePost(MethodView):
    def post(self, id):
        db_session = Database.connect_database()
        
        Posts.delete_post(db_session, id)
        
        db_session.close()
        return redirect(url_for('index'))