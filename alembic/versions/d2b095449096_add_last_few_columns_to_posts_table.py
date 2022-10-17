"""add last few columns to posts table

Revision ID: d2b095449096
Revises: 96ef5f2db747
Create Date: 2022-10-12 23:27:15.840347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2b095449096'
down_revision = '96ef5f2db747'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="True"),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
