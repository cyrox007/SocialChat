from flask.views import MethodView
from flask import render_template, session, redirect, url_for, request
from components.auth.decorator import login_required
from components.user.model import User
from components.blog.model import Posts


class MainPage(MethodView):
    @login_required
    def get(self):
        userdata = User.login(session['login'])
        posts = Posts.get_posts(userdata.id)
        return render_template(
            'home/index.html', 
            user_id=userdata.id, 
            posts=posts
            )


class CreatePost(MethodView):
    @login_required
    def get(self):
        return render_template('home/create.html')

    @login_required
    def post(self):
        title = request.form.get('title')
        body = request.form.get('body')
        if title is None or body is None:
            pass
        userdata = User.login(session['login'])
        Posts.insert_new_post(title=title, text=body, author=userdata.id)
        return redirect(url_for('index'))


class UpdatePost(MethodView):
    @login_required
    def get(self, id):
        user_id = User.get_user_id(session['login'])
        post = Posts.get_post(id=id)
        if user_id != post.author_id:
            print(user_id)
            print(post.author_id)
            return 

        return render_template('blog/update.html', post=post)

    def post(self, id):
        title = request.form.get('title')
        body = request.form.get('body')
        Posts.update_post(id=id, title=title, text=body)
        return redirect(url_for('index'))


class DeletePost(MethodView):
    @login_required
    def get(self, id):
        pass

    def post(self, id):
        Posts.delete_post(id=id)
        return redirect(url_for('index'))