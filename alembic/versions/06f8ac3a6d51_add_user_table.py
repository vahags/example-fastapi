"""add user table

Revision ID: 06f8ac3a6d51
Revises: 6a7601b9ae2f
Create Date: 2022-10-12 16:46:41.877833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06f8ac3a6d51'
down_revision = '6a7601b9ae2f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
    pass
