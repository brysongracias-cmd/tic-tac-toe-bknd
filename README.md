# tic-tac-toe-bknd

Version: 0.1.0

A simple FastAPI backend for a tic-tac-toe game. It provides JWT authentication, game CRUD, and a move endpoint that validates occupied cells, wins, and draws.

## Stack

- FastAPI
- MongoDB with Motor/PyMongo
- Pydantic v2
- JWT authentication with python-jose
- Password hashing with passlib and bcrypt
- Pytest + httpx ASGI transport

## Environment

This project intentionally uses the isolated env file:

```bash
.env_5aed5591dc897f4e
```

Important variables:

```bash
MONGO_URL=mongodb://localhost:27017
MONGO_DATABASE=tic_tac_toe_imp
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PORT=39693
```

The application connects to MongoDB at startup and creates the required collection indexes. In isolated local/CI environments without a Mongo daemon, it falls back to an in-memory repository so API tests and health checks remain runnable.

## Run locally

```bash
chmod +x ./start.sh
PORT=39693 bash ./start.sh
```

API docs:

- http://localhost:39693/docs
- http://localhost:39693/redoc
- http://localhost:39693/health

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

Tests exercise the FastAPI app through ASGI transport and clear the Mongo repository between tests.

## Docker

```bash
docker compose up --build
```

Docker Compose starts a MongoDB service and passes `MONGO_URL=mongodb://mongo:27017` to the API container.

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
