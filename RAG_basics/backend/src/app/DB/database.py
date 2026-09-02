from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine(
    getenv("DATABASE_URL", "sqlite:///./school_rag.db"),
    connect_args={"check_same_thread": False},
)

sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    with sessionlocal() as db:
        yield db


class Base(DeclarativeBase):
    pass
