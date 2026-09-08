# tic-tac-toe-bknd

Version: 0.1.0

A simple production-ready FastAPI backend for a tic-tac-toe game. It provides JWT authentication, game CRUD, and a move endpoint that validates turn order, occupied cells, wins, and draws.

## Stack

- FastAPI
- SQLAlchemy 2.x async ORM
- PostgreSQL with asyncpg
- Pydantic v2
- JWT authentication with python-jose
- Password hashing with passlib and bcrypt
- Pytest + httpx ASGI transport

## Environment

This project intentionally uses the isolated env file:

```bash
.env_93882a75-762a-45f3-a2b2-f23fdc62ca0d
```

Important variables:

```bash
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=20468
```

The configured database is the verified fallback database `gen_ff84970ff5`.

## Run locally

```bash
chmod +x ./start.sh
PORT=20468 bash ./start.sh
```

Windows:

```bat
set PORT=20468 && start /B .\start.bat
```

API docs:

- http://localhost:20468/docs
- http://localhost:20468/redoc
- http://localhost:20468/health

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

Tests use a real PostgreSQL database named by appending `_test` to the configured database name.

## Docker

```bash
docker compose up --build
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/` | Root status |
| POST | `/api/v1/auth/register` | Register a player account |
| POST | `/api/v1/auth/login` | Login and receive a JWT access token |
| GET | `/api/v1/auth/me` | Read the authenticated user |
| POST | `/api/v1/games/` | Create a new tic-tac-toe game |
| GET | `/api/v1/games/` | List authenticated user's games with offset pagination |
| GET | `/api/v1/games/{game_id}` | Read a game |
| PATCH | `/api/v1/games/{game_id}` | Update a game |
| DELETE | `/api/v1/games/{game_id}` | Delete a game |
| POST | `/api/v1/games/{game_id}/moves` | Make the next move |

## Project tree

```text
app/
  core/
    auth.py
    security.py
  routers/
    auth.py
    games.py
  database.py
  main.py
  models.py
  schemas.py
tests/
  conftest.py
  test_auth.py
  test_games.py
  utils/factories.py
seed.py
requirements.txt
start.sh
start.bat
Dockerfile
docker-compose.yml
Makefile
```
