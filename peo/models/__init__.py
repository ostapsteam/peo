from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class Proto():
    __tablename__ = "labs"

    name = sa.Column(sa.String, nullable=False, server_default='')
    desc = sa.Column(sa.Text)

    created_at = sa.Column(sa.DateTime, nullable=False, server_default='')
    updated_at = sa.Column(sa.DateTime)
    deleted_at = sa.Column(sa.DateTime)