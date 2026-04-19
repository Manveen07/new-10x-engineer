"""initial schema

Revision ID: 001
Revises: 
Create Date: 2026-04-19 21:20:00.000000

"""
from typing import Sequence, Optional

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Optional[str] = None
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    # 1. Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # 2. Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('source_uri', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('content_sha256', sa.String(), nullable=False),
        sa.Column('corpus_version', sa.String(), server_default='v1', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_content_sha256', 'documents', ['content_sha256'], unique=False)
    op.create_index('ix_documents_tenant_id', 'documents', ['tenant_id'], unique=False)
    op.create_index('ix_documents_tenant_sha', 'documents', ['tenant_id', 'content_sha256'], unique=True)

    # 3. Create chunks table
    op.create_table(
        'chunks',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('document_id', sa.BigInteger(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('token_count', sa.Integer(), nullable=False),
        sa.Column('splitter_type', sa.String(), server_default='recursive', nullable=False),
        sa.Column('chunk_overlap', sa.Integer(), server_default='0', nullable=False),
        sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('fts', postgresql.TSVECTOR(), nullable=True),
        sa.Column('embedding', Vector(dim=1536), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_chunks_doc_id', 'chunks', ['document_id'], unique=False)
    op.create_index('ix_chunks_fts', 'chunks', ['fts'], unique=False, postgresql_using='gin')
    op.create_index('ix_chunks_tenant_id', 'chunks', ['tenant_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_chunks_tenant_id', table_name='chunks')
    op.drop_index('ix_chunks_fts', table_name='chunks', postgresql_using='gin')
    op.drop_index('ix_chunks_doc_id', table_name='chunks')
    op.drop_table('chunks')
    op.drop_index('ix_documents_tenant_sha', table_name='documents')
    op.drop_index('ix_documents_tenant_id', table_name='documents')
    op.drop_index('ix_documents_content_sha256', table_name='documents')
    op.drop_table('documents')
    op.execute("DROP EXTENSION IF EXISTS vector")
