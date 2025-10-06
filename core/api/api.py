from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .routers import user

app = FastAPI()

# Монтируем статические файлы админки
admin_assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'admin', 'assets', 'static')
app.mount('/admin/static', StaticFiles(directory=admin_assets_dir), name='admin_static')

app.include_router(user.router, prefix='/users')
