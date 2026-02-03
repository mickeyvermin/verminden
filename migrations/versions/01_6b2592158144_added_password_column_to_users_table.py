"""Added 'password' column to 'users' table

Revision ID: 6b2592158144
Revises:
Create Date: 2026-01-28 10:10:55.815418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6b2592158144"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("password", sa.String(20), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "password")
