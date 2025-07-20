"""add_document_generation_tables

Revision ID: 05c2726bd694
Revises: 41dc18e5fc9e
Create Date: 2025-07-21 03:43:16.039131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05c2726bd694'
down_revision: Union[str, Sequence[str], None] = '41dc18e5fc9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create business_proposals table
    op.create_table(
        'business_proposals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('client_name', sa.String(), nullable=False),
        sa.Column('project_title', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_business_proposals_id'), 'business_proposals', ['id'], unique=False)

    # Create partnership_agreements table
    op.create_table(
        'partnership_agreements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('party1_name', sa.String(), nullable=False),
        sa.Column('party2_name', sa.String(), nullable=False),
        sa.Column('partnership_purpose', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_partnership_agreements_id'), 'partnership_agreements', ['id'], unique=False)

    # Create ndas table
    op.create_table(
        'ndas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('disclosing_party', sa.String(), nullable=False),
        sa.Column('receiving_party', sa.String(), nullable=False),
        sa.Column('purpose', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_ndas_id'), 'ndas', ['id'], unique=False)

    # Create contracts table
    op.create_table(
        'contracts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contract_type', sa.String(), nullable=False),
        sa.Column('party1_name', sa.String(), nullable=False),
        sa.Column('party2_name', sa.String(), nullable=False),
        sa.Column('service_description', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_contracts_id'), 'contracts', ['id'], unique=False)

    # Create terms_of_service table
    op.create_table(
        'terms_of_service',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('website_url', sa.String(), nullable=False),
        sa.Column('service_description', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_terms_of_service_id'), 'terms_of_service', ['id'], unique=False)

    # Create privacy_policies table
    op.create_table(
        'privacy_policies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('website_url', sa.String(), nullable=False),
        sa.Column('ai_generated_content', sa.Text(), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False),
        sa.Column('docs_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )
    op.create_index(op.f('ix_privacy_policies_id'), 'privacy_policies', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop all document generation tables
    op.drop_index(op.f('ix_privacy_policies_id'), table_name='privacy_policies')
    op.drop_table('privacy_policies')
    op.drop_index(op.f('ix_terms_of_service_id'), table_name='terms_of_service')
    op.drop_table('terms_of_service')
    op.drop_index(op.f('ix_contracts_id'), table_name='contracts')
    op.drop_table('contracts')
    op.drop_index(op.f('ix_ndas_id'), table_name='ndas')
    op.drop_table('ndas')
    op.drop_index(op.f('ix_partnership_agreements_id'), table_name='partnership_agreements')
    op.drop_table('partnership_agreements')
    op.drop_index(op.f('ix_business_proposals_id'), table_name='business_proposals')
    op.drop_table('business_proposals')
