import os

os.environ.update(
    {
        'APP_ENV': 'test',
        'ADMIN_ENABLED': 'false',
        'DATABASE_URL': 'postgresql+asyncpg://postgres:postgres@localhost/test',
        'SECRET_KEY': 'test-secret-key-that-is-at-least-32-characters',
        'ADMIN_USERNAME': 'admin',
        'ADMIN_PASSWORD': 'test-admin-password',
    }
)
