"""add foreign key to posts table

Revision ID: 96ef5f2db747
Revises: 06f8ac3a6d51
Create Date: 2022-10-12 18:18:59.480223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96ef5f2db747'
down_revision = '06f8ac3a6d51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
