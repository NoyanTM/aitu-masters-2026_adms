from contextlib import contextmanager 

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import SQLAlchemyError

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    # metadata = MetaData(naming_convention=convention)
    pass


@contextmanager
def get_session(url: str):
    engine = create_engine(url, echo=True)
    session = sessionmaker(bind=engine)
    session_local = session()
    try:
        yield session_local
    except SQLAlchemyError as e:
        print(e)
    finally:
        session_local.close()
