from views.auth import views


def install(app):
    app.add_url_rule(
        '/login',
        view_func=views.LoginPage.as_view('login')
    )
    app.add_url_rule(
        '/register',
        view_func=views.RegisterPage.as_view('auth.register')
    )
    app.add_url_rule(
        '/logout',
        view_func=views.LogoutUser.as_view('auth.logout')
    )