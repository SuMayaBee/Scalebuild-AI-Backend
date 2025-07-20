"""add_logos_table

Revision ID: 41dc18e5fc9e
Revises: a751d844a901
Create Date: 2025-07-20 21:18:00.653545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41dc18e5fc9e'
down_revision: Union[str, Sequence[str], None] = 'a751d844a901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create logos table
    op.create_table(
        'logos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('logo_image_url', sa.String(), nullable=False),
        sa.Column('remove_bg_logo_image_url', sa.String(), nullable=True),
        sa.Column('content', sa.JSON(), nullable=True),
        sa.Column('logo_title', sa.String(), nullable=False),
        sa.Column('logo_vision', sa.String(), nullable=True),
        sa.Column('color_palette_name', sa.String(), nullable=True),
        sa.Column('logo_style', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_logos_id'), 'logos', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop logos table
    op.drop_index(op.f('ix_logos_id'), table_name='logos')
    op.drop_table('logos')
