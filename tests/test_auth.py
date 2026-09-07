# Tests for authentication API endpoints.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
import pytest

from tests.utils.factories import user_payload

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_register(client):
    response = await client.post("/api/v1/auth/register", json=user_payload())
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["email"].endswith("@example.com")


async def test_login(client):
    payload = user_payload()
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/login", data={"username": payload["username"], "password": payload["password"]})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


async def test_me(client):
    payload = user_payload()
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", data={"username": payload["username"], "password": payload["password"]})
    token = login.json()["access_token"]
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == payload["username"]


async def test_invalid_token(client):
    response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
