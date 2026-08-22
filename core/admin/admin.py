from pathlib import Path

from fastapi import FastAPI
from sqladmin import Admin

from ..orm import engine
from ..settings import settings
from .auth import authentication_backend
from .views import ThingAdmin, UserAdmin

ASSETS_DIR = Path(__file__).parent / 'assets'


def create_admin(app: FastAPI) -> Admin:
    admin = Admin(
        app,
        engine,
        title=settings.APP_NAME,
        authentication_backend=authentication_backend,
        templates_dir=str(ASSETS_DIR / 'templates'),
    )
    admin.add_view(UserAdmin)
    admin.add_view(ThingAdmin)
    return admin
