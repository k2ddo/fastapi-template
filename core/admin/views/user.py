from sqladmin import ModelView

from ...orm.models import User


class UserAdmin(ModelView, model=User):
    name = 'Пользователь'
    name_plural = 'Пользователи'

    column_labels = {
        User.username: 'Никнейм',
        User.first_name: 'Имя',
    }
    column_list = [User.username, User.first_name]
    column_details_list = [User.id, User.username, User.first_name, User.last_name]
    form_excluded_columns = [User.password]
    can_create = False
    can_edit = False
