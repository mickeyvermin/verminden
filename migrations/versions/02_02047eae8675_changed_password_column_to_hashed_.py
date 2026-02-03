"""Changed 'password' column to 'hashed_password' in 'users' table

Revision ID: 02047eae8675
Revises: 6b2592158144
Create Date: 2026-02-02 15:16:58.372820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02047eae8675"
down_revision: Union[str, Sequence[str], None] = "6b2592158144"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("users", "password", new_column_name="hashed_password")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("users", "hashed_password", new_column_name="password")
