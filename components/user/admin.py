from flask_admin.contrib.sqla import ModelView

from components.user import model

class UserModelView(ModelView):
    column_default_sort = ('id', True)
    column_labels = dict(
        username="Логин"
    )
    column_list = (
        'id',
        'username',
    )
    column_editable_list = (
        'username',
    )
    form_columns = (
        'username',
    )


def load_views(admin, session):
    admin.add_view(UserModelView(model.User, session, name='Пользователи'))
    session.close()