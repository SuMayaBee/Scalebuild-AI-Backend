"""restore_dropped_tables

Revision ID: 3c0700de9716
Revises: fd556464aa32
Create Date: 2025-08-07 08:05:33.498292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c0700de9716'
down_revision: Union[str, Sequence[str], None] = 'fd556464aa32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Restore all the dropped tables."""
    from sqlalchemy.dialects import postgresql
    
    # Restore logos table
    op.create_table('logos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('logo_image_url', sa.String(), nullable=False),
        sa.Column('remove_bg_logo_image_url', sa.String(), nullable=True),
        sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('logo_title', sa.String(), nullable=False),
        sa.Column('logo_vision', sa.String(), nullable=True),
        sa.Column('color_palette_name', sa.String(), nullable=True),
        sa.Column('logo_style', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_logos_id'), 'logos', ['id'], unique=False)
    
    # Restore short_videos table
    op.create_table('short_videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=False),
        sa.Column('aspect_ratio', sa.String(), nullable=True),
        sa.Column('duration', sa.String(), nullable=True),
        sa.Column('audio_generation', sa.Boolean(), nullable=True),
        sa.Column('watermark', sa.Boolean(), nullable=True),
        sa.Column('person_generation', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_short_videos_id'), 'short_videos', ['id'], unique=False)
    
    # Restore business_proposals table
    op.create_table('business_proposals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('client_name', sa.String(), nullable=False),
        sa.Column('project_title', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_business_proposals_id'), 'business_proposals', ['id'], unique=False)
    
    # Restore contracts table
    op.create_table('contracts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contract_type', sa.String(), nullable=False),
        sa.Column('party1_name', sa.String(), nullable=False),
        sa.Column('party2_name', sa.String(), nullable=False),
        sa.Column('service_description', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contracts_id'), 'contracts', ['id'], unique=False)
    
    # Restore ndas table
    op.create_table('ndas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('disclosing_party', sa.String(), nullable=False),
        sa.Column('receiving_party', sa.String(), nullable=False),
        sa.Column('purpose', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ndas_id'), 'ndas', ['id'], unique=False)
    
    # Restore partnership_agreements table
    op.create_table('partnership_agreements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('party1_name', sa.String(), nullable=False),
        sa.Column('party2_name', sa.String(), nullable=False),
        sa.Column('partnership_purpose', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_partnership_agreements_id'), 'partnership_agreements', ['id'], unique=False)
    
    # Restore privacy_policies table
    op.create_table('privacy_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('website_url', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_privacy_policies_id'), 'privacy_policies', ['id'], unique=False)
    
    # Restore terms_of_service table
    op.create_table('terms_of_service',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('website_url', sa.String(), nullable=False),
        sa.Column('service_description', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_terms_of_service_id'), 'terms_of_service', ['id'], unique=False)


def downgrade() -> None:
    """Drop the restored tables."""
    op.drop_index(op.f('ix_terms_of_service_id'), table_name='terms_of_service')
    op.drop_table('terms_of_service')
    op.drop_index(op.f('ix_privacy_policies_id'), table_name='privacy_policies')
    op.drop_table('privacy_policies')
    op.drop_index(op.f('ix_partnership_agreements_id'), table_name='partnership_agreements')
    op.drop_table('partnership_agreements')
    op.drop_index(op.f('ix_ndas_id'), table_name='ndas')
    op.drop_table('ndas')
    op.drop_index(op.f('ix_contracts_id'), table_name='contracts')
    op.drop_table('contracts')
    op.drop_index(op.f('ix_business_proposals_id'), table_name='business_proposals')
    op.drop_table('business_proposals')
    op.drop_index(op.f('ix_short_videos_id'), table_name='short_videos')
    op.drop_table('short_videos')
    op.drop_index(op.f('ix_logos_id'), table_name='logos')
    op.drop_table('logos')
