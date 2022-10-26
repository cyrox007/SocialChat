from views.profile import views

def install(app):
    app.add_url_rule(
        '/profile/<string:login>',
        view_func=views.ProfilePage.as_view('profile.index')
    )
    app.add_url_rule(
        '/profile/<string:login>/edit',
        view_func=views.EditProfile.as_view('profile.edit')
    )
    app.add_url_rule(
        '/profile/<string:login>/substract',
        view_func=views.SubstractAuthor.as_view('profile.substract')
    )
    app.add_url_rule(
        '/profile/<string:login>/unsubscribe',
        view_func=views.UnsubscribeAuthor.as_view('profile.unsubscribe')
    )