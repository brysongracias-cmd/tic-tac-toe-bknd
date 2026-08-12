# Pytest fixtures using FastAPI ASGI transport and the MongoDB repository.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
import pytest
from httpx import ASGITransport, AsyncClient

from app.database import get_db, store
from app.main import app


@pytest.fixture
async def db_session():
    store.in_memory = True
    await store.clear()
    yield store
    await store.clear()


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
