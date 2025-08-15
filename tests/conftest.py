import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from helpers import router
from helpers.db import Base, get_session  # importa a função de dependência real

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

TestingAsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    future=True,
)


@pytest_asyncio.fixture(scope="function")
async def db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def app(db) -> FastAPI:
    app = FastAPI()
    router.setup(app)

    async def override_get_session():
        async with TestingAsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
