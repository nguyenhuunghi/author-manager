"""empty message

Revision ID: 1651182da7ff
Revises: 
Create Date: 2020-12-17 14:16:43.537681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1651182da7ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=120), nullable=False, server_default='_blank'))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
