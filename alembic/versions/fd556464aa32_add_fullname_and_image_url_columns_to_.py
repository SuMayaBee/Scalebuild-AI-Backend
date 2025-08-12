"""add_fullname_and_image_url_columns_to_users

Revision ID: fd556464aa32
Revises: 5383747650d1
Create Date: 2025-08-07 07:51:33.893678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd556464aa32'
down_revision: Union[str, Sequence[str], None] = '5383747650d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename 'name' column to 'fullname'
    op.alter_column('users', 'name', new_column_name='fullname')
    
    # Rename 'image' column to 'image_url'
    op.alter_column('users', 'image', new_column_name='image_url')


def downgrade() -> None:
    """Downgrade schema."""
    # Rename back to original column names
    op.alter_column('users', 'image_url', new_column_name='image')
    op.alter_column('users', 'fullname', new_column_name='name')
