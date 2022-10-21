from views.profile import views

def install(app):
    app.add_url_rule(
        '/profile/<string:login>',
        view_func=views.ProfilePage.as_view('profile.index')
    )