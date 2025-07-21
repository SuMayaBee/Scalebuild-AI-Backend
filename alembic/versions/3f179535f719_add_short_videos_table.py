"""add_short_videos_table

Revision ID: 3f179535f719
Revises: 05c2726bd694
Create Date: 2025-07-21 06:17:36.608640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f179535f719'
down_revision: Union[str, Sequence[str], None] = '05c2726bd694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create short_videos table
    op.create_table(
        'short_videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=False),
        sa.Column('aspect_ratio', sa.String(), nullable=True, default='16:9'),
        sa.Column('duration', sa.String(), nullable=True, default='8'),
        sa.Column('audio_generation', sa.Boolean(), nullable=True, default=True),
        sa.Column('watermark', sa.Boolean(), nullable=True, default=True),
        sa.Column('person_generation', sa.String(), nullable=True, default='allow_all'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_short_videos_id'), 'short_videos', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop short_videos table
    op.drop_index(op.f('ix_short_videos_id'), table_name='short_videos')
    op.drop_table('short_videos')
