"""merge heads

Revision ID: fa3e3a5ee5d9
Revises: 3c0700de9716, add_reset_token_expires
Create Date: 2025-08-12 15:11:22.843554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa3e3a5ee5d9'
down_revision: Union[str, Sequence[str], None] = ('3c0700de9716', 'add_reset_token_expires')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
