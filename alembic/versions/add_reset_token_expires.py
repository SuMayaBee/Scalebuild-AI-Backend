"""add reset token expires field

Revision ID: add_reset_token_expires
Revises: fd556464aa32
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_reset_token_expires'
down_revision = 'fd556464aa32'
branch_labels = None
depends_on = None


def upgrade():
    # Add reset_token_expires column to users table
    op.add_column('users', sa.Column('reset_token_expires', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # Remove reset_token_expires column from users table
    op.drop_column('users', 'reset_token_expires')