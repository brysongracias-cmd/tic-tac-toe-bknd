# Tests for tic-tac-toe game CRUD and move API endpoints.
from dotenv import load_dotenv
load_dotenv('.env_93882a75-762a-45f3-a2b2-f23fdc62ca0d', override=True)
import pytest

from tests.utils.factories import game_payload, move_payload

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_game(client, auth_headers):
    response = await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["board"] == ["", "", "", "", "", "", "", "", ""]
    assert body["current_player"] == "X"
    assert body["status"] == "in_progress"


async def test_list_games(client, auth_headers):
    await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    response = await client.get("/api/v1/games/?offset=0&limit=20", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_game(client, auth_headers):
    created = await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    game_id = created.json()["id"]
    response = await client.get(f"/api/v1/games/{game_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == game_id


async def test_update_game(client, auth_headers):
    created = await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    game_id = created.json()["id"]
    payload = {"board": ["X", "", "", "", "", "", "", "", ""], "current_player": "O"}
    response = await client.patch(f"/api/v1/games/{game_id}", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["board"][0] == "X"
    assert response.json()["current_player"] == "O"


async def test_delete_game(client, auth_headers):
    created = await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    game_id = created.json()["id"]
    deleted = await client.delete(f"/api/v1/games/{game_id}", headers=auth_headers)
    assert deleted.status_code == 204
    missing = await client.get(f"/api/v1/games/{game_id}", headers=auth_headers)
    assert missing.status_code == 404


async def test_make_move(client, auth_headers):
    created = await client.post("/api/v1/games/", json=game_payload(), headers=auth_headers)
    game_id = created.json()["id"]
    response = await client.post(f"/api/v1/games/{game_id}/moves", json=move_payload(0), headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["board"][0] == "X"
    assert body["current_player"] == "O"
    assert len(body["moves"]) == 1
