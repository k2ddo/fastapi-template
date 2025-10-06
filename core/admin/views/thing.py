from sqladmin import ModelView

from ...orm.models import Thing


class ThingAdmin(ModelView, model=Thing):
    name = 'Вещь'
    name_plural = 'Вещи'

    column_labels = {
        Thing.name: 'Название',
        Thing.owner: 'Пользователь',
    }
    column_list = [Thing.name, Thing.owner]
