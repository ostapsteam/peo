from sqlalchemy.orm import sessionmaker, Query
from contextlib import contextmanager


class BaseQuery(Query):
    def not_deleted(self, model_class):
        return self.filter(model_class.deleted_at.isnot(None))


class DB:
    Session = None

    @classmethod
    def configure(cls, engine):
        cls.Session = sessionmaker(bind=engine, query_cls=BaseQuery, expire_on_commit=False)

    @classmethod
    @contextmanager
    def session(cls):
        assert cls.Session, "SQLAlchemy engine is not set"
        s = cls.Session()
        try:
            yield s
            s.flush()
            s.commit()
        except:
            s.rollback()
            raise
        finally:
            s.close()