import sqlalchemy as sa
from sqlalchemy import orm

from peo.models import Base, Thing
from marshmallow import Schema, fields


class Lab(Base, Thing):

    __tablename__ = "labs"

    class DoesNotExist(Exception):
        pass

    class NameAlreadyInUse(Exception):
        pass

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(length=254), unique=True, nullable=False)

    def __repr__(self):
        return "Lab #{}".format(self.id)

    @staticmethod
    def get(session, lid, with_deleted=False):
        lab = session.query(Lab).get(lid)
        if lab and not(lab.is_deleted() and not with_deleted):
            return lab
        raise Lab.DoesNotExist

    @staticmethod
    def get_by_name(session, name, with_deleted=False):
        return session.query(Lab).filter(
            Lab.name == name
        ).first()

    def set_name(self, name):
        if self.name != name:
            session = orm.object_session(self)
            assert session is not None, "Lab has no attached session"
            another_lab = Lab.get_by_name(session, name)
            if another_lab and another_lab.id != self.id:
                raise Lab.NameAlreadyInUse
            self.name = name


class LabSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    desc = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime()