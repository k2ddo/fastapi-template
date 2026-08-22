import pytest
from pydantic import ValidationError

from core.settings.settings import Settings


def test_rejects_short_secrets() -> None:
    with pytest.raises(ValidationError):
        Settings.model_validate(
            {
                'SECRET_KEY': 'short',
                'ADMIN_USERNAME': 'admin',
                'ADMIN_PASSWORD': 'short',
            }
        )
