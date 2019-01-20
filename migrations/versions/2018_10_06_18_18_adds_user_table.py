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
        sa.Column('first_name', sa.String(length=128), nullable=False),
        sa.Column('last_name', sa.String(length=128), nullable=False),
        sa.Column('primary_email_fk', sa.String(length=128), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('primary_email_fk')
    )

    op.create_table('emails',
        sa.Column('email', sa.String(length=128), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('verified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'],
                                name='fk_email_user_id', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('email', 'user_id')
    )
    op.create_index(op.f('ix_emails_email'), 'emails', ['email'], unique=True)

    op.create_foreign_key('fk_user_id_primary_email', 'users', 'emails',
                          ['primary_email_fk', 'id'], ['email', 'user_id'],
                          ondelete='RESTRICT')

    connection = op.get_bind()

    connection.execute("""
        CREATE TRIGGER enforce_verified_primary_email_on_update BEFORE UPDATE ON users
            FOR EACH ROW
            BEGIN
                IF (SELECT COUNT(email) FROM emails
                        WHERE emails.email = NEW.primary_email_fk
                        AND emails.verified = 1) != 1
                THEN
                    SIGNAL SQLSTATE '45000' SET message_text = 'Primary email must exist in emails table and be a verified email.';
                END IF;
            END;
    """)

    connection.execute("""
        CREATE TRIGGER enforce_email_immutability_on_update BEFORE UPDATE ON emails
            FOR EACH ROW
            BEGIN
                IF NEW.email != OLD.email OR NEW.user_id != OLD.user_id
                THEN
                    SIGNAL SQLSTATE '45000' SET message_text = 'Email is immutable and cannot be changed.';
                END IF;
            END;
    """)


def downgrade():
    op.drop_index(op.f('ix_emails_email'), table_name='emails')
    op.drop_constraint('fk_email_user_id', 'emails', type_='foreignkey')
    op.drop_constraint('fk_user_id_primary_email', 'users', type_='foreignkey')

    connection = op.get_bind()

    connection.execute("DROP TRIGGER IF EXISTS enforce_verified_primary_email_on_update")
    connection.execute("DROP TRIGGER IF EXISTS enforce_email_immutability_on_update")

    op.drop_table('users')
    op.drop_table('emails')
