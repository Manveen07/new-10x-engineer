"""add chunk ordering constraint

Revision ID: 002
Revises: 001
Create Date: 2026-04-19 22:00:00.000000

"""
from typing import Sequence, Optional

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Optional[str] = '001'
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    op.create_index('ix_chunks_doc_index', 'chunks', ['document_id', 'chunk_index'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_chunks_doc_index', table_name='chunks')
