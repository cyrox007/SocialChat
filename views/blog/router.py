from views.blog import views


def install(app):
    app.add_url_rule(
        '/',
        view_func=views.MainPage.as_view('index')
    )
    app.add_url_rule(
        '/create',
        view_func=views.CreatePost.as_view('blog.create')
    )
    app.add_url_rule(
        '/<int:id>/update',
        view_func=views.UpdatePost.as_view('blog.update')
    )
    app.add_url_rule(
        '/<int:id>/delete',
        view_func=views.DeletePost.as_view('blog.delete')
    )