# -*- coding: utf-8 -*-

"""
adds user table
~~~~~~~~~~~~~~~~~~~~~~

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
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('first_name', sa.String(length=128), nullable=True),
        sa.Column('last_name', sa.String(length=128), nullable=True),
        sa.Column('primary_email', sa.String(length=128), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('primary_email')
    )

    op.create_table('emails',
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('email', 'user_id')
    )
    op.create_index(op.f('ix_emails_email'), 'emails', ['email'], unique=False)

    op.create_foreign_key('fk_user_primary_email', 'users', 'emails',
                          ['id', 'primary_email'], ['user_id', 'email'],
                          ondelete='RESTRICT')

def downgrade():
    op.drop_index(op.f('ix_emails_email'), table_name='emails')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_table('users')
    op.drop_table('emails')
