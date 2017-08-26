import sqlalchemy as sa
from peo.models import Base, Proto
from marshmallow import Schema, fields, pprint


class Lab(Base, Proto):

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


class LabSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    desc = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    deleted_at = fields.DateTime()