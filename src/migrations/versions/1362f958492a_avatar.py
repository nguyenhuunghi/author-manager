"""avatar

Revision ID: 1362f958492a
Revises: 1651182da7ff
Create Date: 2020-12-17 18:06:18.790100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1362f958492a'
down_revision = '1651182da7ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authors', sa.Column('avatar', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authors', 'avatar')
    # ### end Alembic commands ###