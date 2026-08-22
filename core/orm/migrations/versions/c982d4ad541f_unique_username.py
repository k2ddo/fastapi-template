"""Make usernames unique.

Revision ID: c982d4ad541f
Revises: b31c5947dd45
Create Date: 2026-08-22 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op

revision: str = 'c982d4ad541f'
down_revision: str | Sequence[str] | None = 'b31c5947dd45'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index('ix_user_username', table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_user_username', table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
