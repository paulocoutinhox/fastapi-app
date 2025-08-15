import logging
import os
from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./app.db"
DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

async_engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=os.environ.get("ECHO_SQL", "false").lower() == "true",
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncIterator[async_sessionmaker]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(f"Database session error: {e}")
            await session.rollback()
            raise


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
