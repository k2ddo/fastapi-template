from sqladmin import Admin
import os

from ..api import app
from ..orm import engine
from .auth import authentication_backend
from .views import ThingAdmin, UserAdmin

# Получаем путь к папке assets относительно текущего файла
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')

admin = Admin(
    app,
    engine,
    title='Шаблон FastAPI',
    authentication_backend=authentication_backend,
    templates_dir=os.path.join(assets_dir, 'templates'),
)
admin.add_view(UserAdmin)
admin.add_view(ThingAdmin)
