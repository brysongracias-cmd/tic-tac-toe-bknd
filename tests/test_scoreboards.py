# Tests for scoreboard creation.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_scoreboard(client):
    response = await client.post("/api/v1/scoreboards/", json={})

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert "created_at" in body
