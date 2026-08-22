from secrets import compare_digest

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from ..settings import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get('username', ''))
        password = str(form.get('password', ''))
        authenticated = compare_digest(username, settings.ADMIN_USERNAME)
        authenticated &= compare_digest(
            password, settings.ADMIN_PASSWORD.get_secret_value()
        )
        if authenticated:
            request.session.update({'authenticated': True})
        return authenticated

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get('authenticated') is True


authentication_backend = AdminAuth(
    secret_key=settings.SECRET_KEY.get_secret_value(),
    session_cookie='admin_session',
    same_site='strict',
    https_only=settings.APP_ENV == 'production',
    max_age=60 * 60 * 8,
)
