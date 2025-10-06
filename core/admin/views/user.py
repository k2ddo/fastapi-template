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
