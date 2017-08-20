from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class DB:
    create_session = None

    @classmethod
    def configure(cls, engine):
        cls.create_session = sessionmaker(bind=engine)

    @classmethod
    @contextmanager
    def __call__(cls):
        assert cls.create_session, "SQLAlchemy engine is not set"
        session = cls.create_session()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()