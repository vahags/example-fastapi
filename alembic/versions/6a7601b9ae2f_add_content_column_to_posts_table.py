"""add content column to posts table

Revision ID: 6a7601b9ae2f
Revises: 2882fca39a01
Create Date: 2022-10-12 05:39:51.827842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a7601b9ae2f'
down_revision = '2882fca39a01'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
