from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from core.api.routers import user
from core.orm import engine
from core.orm.admin import UserAdmin
from core.orm.admin.auth import authentication_backend

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
admin = Admin(
    app,
    engine,
    title='Шаблон FastAPI',
    authentication_backend=authentication_backend,
)
admin.add_view(UserAdmin)

app.include_router(user.router, prefix='/users')
