# Pytest fixtures using a real PostgreSQL database and ASGI transport.
import os
from urllib.parse import urlsplit, urlunsplit

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
import asyncpg
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.database import Base, get_db
from app.main import app
from app.models import *  # noqa: F401,F403

MAIN_DB_URL = os.getenv("DATABASE_URL", "")
_parts = MAIN_DB_URL.rsplit("/", 1)
TEST_DB_URL = (_parts[0] + "/" + _parts[1] + "_test") if len(_parts) == 2 else MAIN_DB_URL


def _asyncpg_url_for_database(db_url: str, database: str) -> str:
    parsed = urlsplit(db_url.replace("postgresql+asyncpg://", "postgresql://", 1))
    return urlunsplit((parsed.scheme, parsed.netloc, "/" + database, "", ""))


async def _ensure_database_exists(db_url: str) -> None:
    url = make_url(db_url)
    database = url.database
    admin_database = "postgres"
    admin_url = _asyncpg_url_for_database(db_url, admin_database)
    conn = await asyncpg.connect(admin_url)
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", database)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{database}"')
    finally:
        await conn.close()


@pytest.fixture(scope="session")
async def db_engine():
    await _ensure_database_exists(MAIN_DB_URL)
    await _ensure_database_exists(TEST_DB_URL)
    main_engine = create_async_engine(MAIN_DB_URL, poolclass=NullPool)
    async with main_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await main_engine.dispose()

    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(client):
    payload = {"email": "fixture@example.com", "username": "fixtureuser", "password": "password123"}
    register = await client.post("/api/v1/auth/register", json=payload)
    assert register.status_code == 201
    login = await client.post("/api/v1/auth/login", data={"username": payload["username"], "password": payload["password"]})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
