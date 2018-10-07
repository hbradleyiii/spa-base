"""adds user table

Revision ID: 197c3ef71f00
Revises:
Create Date: 2018-10-06 18:18:32.510349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '197c3ef71f00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
                  sa.PrimaryKeyConstraint('id'),
        sa.Column('first_name', sa.String(length=128), nullable=True),
        sa.Column('last_name', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'],
                    unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
