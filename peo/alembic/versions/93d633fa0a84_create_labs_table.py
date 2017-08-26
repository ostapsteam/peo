"""Create labs table

Revision ID: 93d633fa0a84
Revises: 
Create Date: 2017-08-23 23:00:58.795061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = '93d633fa0a84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "labs",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=254), nullable=False, unique=True),
        sa.Column("desc", sa.Text),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=func.now()),
        sa.Column("updated_at", sa.DateTime, onupdate=func.now()),
        sa.Column("deleted_at", sa.DateTime)
    )


def downgrade():
    op.drop_table("labs")
