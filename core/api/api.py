from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from ..admin import create_admin
from ..orm.database import engine
from ..settings import settings
from ..settings.logging import configure_logging
from .routers import auth, health, user

ADMIN_STATIC_DIR = Path(__file__).parents[1] / 'admin' / 'assets' / 'static'
configure_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version='0.1.0',
        lifespan=lifespan,
        openapi_url='/openapi.json' if settings.APP_ENV != 'production' else None,
        docs_url='/docs' if settings.APP_ENV != 'production' else None,
        redoc_url='/redoc' if settings.APP_ENV != 'production' else None,
    )

    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
    if settings.ALLOWED_HOSTS != ['*']:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    app.include_router(health.router)
    app.include_router(auth.router, prefix=settings.API_PREFIX)
    app.include_router(user.router, prefix=settings.API_PREFIX)

    if settings.ADMIN_ENABLED:
        app.mount(
            '/admin/static',
            StaticFiles(directory=ADMIN_STATIC_DIR),
            name='admin_static',
        )
        create_admin(app)

    return app


app = create_app()
