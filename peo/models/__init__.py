from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime

Base = declarative_base()


class Proto():
    created_at = sa.Column(sa.DateTime, nullable=False, server_default=func.now())
    updated_at = sa.Column(sa.DateTime, onupdate=func.now())
    deleted_at = sa.Column(sa.DateTime)

    def is_deleted(self):
        return self.deleted_at is not None

    def delete(self):
        if not self.is_deleted():
            self.deleted_at = datetime.utcnow()


class Thing(Proto):
    name = sa.Column(sa.String(length=254), nullable=False, server_default='')
    desc = sa.Column(sa.Text)


class GeoThing(Thing):
    lat = sa.Column(sa.Numeric(10, 10, asdecimal=True))
    lon = sa.Column(sa.Numeric(10, 10, asdecimal=True))