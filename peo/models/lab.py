import sqlalchemy as sa
from  . import Base, Proto


class Lab(Base, Proto):
    id = sa.Column(sa.Integer, primary_key=True)

    def __repr__(self):
        return "Lab #{}".format(self.id)