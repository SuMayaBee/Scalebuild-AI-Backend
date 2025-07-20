"""add_presentation_images_table

Revision ID: a751d844a901
Revises: a7288df21b05
Create Date: 2025-07-20 19:36:14.643828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a751d844a901'
down_revision: Union[str, Sequence[str], None] = 'a7288df21b05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create presentation_images table
    op.create_table(
        'presentation_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('presentation_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=False),
        sa.Column('filename', sa.String(), nullable=True),
        sa.Column('model', sa.String(), nullable=True, default='dall-e-3'),
        sa.Column('size', sa.String(), nullable=True, default='1024x1024'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['presentation_id'], ['presentations.id'], ),
    )
    op.create_index(op.f('ix_presentation_images_id'), 'presentation_images', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop presentation_images table
    op.drop_index(op.f('ix_presentation_images_id'), table_name='presentation_images')
    op.drop_table('presentation_images')
