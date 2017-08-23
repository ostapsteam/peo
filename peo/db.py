from sqlalchemy.orm import sessionmaker, Query
from contextlib import contextmanager


class BaseQuery(Query):
    def not_deleted(self, model_class):
        return self.filter(model_class.deleted_at.isnot(None))


class DB:
    Session = None

    @classmethod
    def configure(cls, engine):
        cls.Session = sessionmaker(bind=engine, query_cls=BaseQuery)

    @classmethod
    @contextmanager
    def session(cls):
        assert cls.Session, "SQLAlchemy engine is not set"
        s = cls.Session()
        try:
            yield s
        except Exception as e:
            print(str(e))
            s.rollback()
            raise
        else:
            s.commit()
        finally:
            s.close()