"""Added accounts table

Revision ID: e397317e3d00
Revises: 93d633fa0a84
Create Date: 2017-08-27 00:47:03.228892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e397317e3d00'
down_revision = '93d633fa0a84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("login", sa.String(length=128), nullable=False, unique=True),
        sa.Column("passwd_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("desc", sa.Text),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=func.now()),
        sa.Column("updated_at", sa.DateTime, onupdate=func.now()),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("last_login", sa.DateTime)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accounts')
    # ### end Alembic commands ###