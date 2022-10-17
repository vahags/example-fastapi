"""create posts table

Revision ID: 2882fca39a01
Revises: 
Create Date: 2022-10-11 21:58:33.660725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2882fca39a01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
