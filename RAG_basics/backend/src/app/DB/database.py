from os import getenv

from sqlalchemy.ext.asyncio import ( AsyncSession, create_async_engine , async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    getenv("DATABASE_URL", "sqlite+aiosqlite:///./school_rag.db"),
    connect_args={"check_same_thread": False},
)

async_sessionlocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


async def get_db():
    async with async_sessionlocal() as db:
        yield db


class Base(DeclarativeBase):
    pass
