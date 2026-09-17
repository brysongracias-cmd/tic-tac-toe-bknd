# Tests for tic-tac-toe game CRUD and move API endpoints.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
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


async def test_add_bot_player_and_play_solo_game(client, auth_headers):
    bot_response = await client.post(
        "/api/v1/bot-players/",
        json={"name": "Solo Bot"},
        headers=auth_headers,
    )
    assert bot_response.status_code == 201
    bot_id = bot_response.json()["id"]

    game_response = await client.post(
        "/api/v1/games/solo",
        json={"bot_player_id": bot_id},
        headers=auth_headers,
    )
    assert game_response.status_code == 201
    game = game_response.json()
    assert game["bot_player_id"] == bot_id

    move_response = await client.post(
        f"/api/v1/games/{game['id']}/moves",
        json={"position": 4},
        headers=auth_headers,
    )
    assert move_response.status_code == 201
    played_game = move_response.json()
    assert played_game["board"][4] == "X"
    assert played_game["board"][0] == "O"
    assert played_game["current_player"] == "X"
    assert len(played_game["moves"]) == 2
