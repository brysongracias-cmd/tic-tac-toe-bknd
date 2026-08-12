COMMIT_MESSAGE: Use MongoDB for tic-tac-toe persistence

## Features Added
- Replaced SQLAlchemy/PostgreSQL persistence with a MongoDB-backed repository using Motor/PyMongo.
- Added MongoDB connection lifecycle handling and collection indexes for users, games, and moves.
- Updated authentication and game endpoints to read and write through the MongoDB repository.
- Added an in-memory fallback for isolated test/server environments where a MongoDB daemon is unavailable.

## Files Modified
- app/database.py — replaced SQLAlchemy engine/session setup with MongoDB connection and repository helpers.
- app/models.py — converted SQLAlchemy ORM models to dataclass domain models while preserving API schema compatibility.
- app/main.py — initializes and closes MongoDB during FastAPI lifespan.
- app/core/auth.py — loads users through MongoDB repository for JWT authentication.
- app/core/security.py — loads SECRET_KEY only from .env_5aed5591dc897f4e instead of a hardcoded source fallback.
- app/routers/auth.py — rewired registration and login to MongoDB user operations.
- app/routers/games.py — rewired game CRUD and move creation to MongoDB game/move operations.
- app/schemas.py — updated dotenv file target to .env_5aed5591dc897f4e.
- seed.py — rewrote seed data creation to use MongoDB repository helpers.
- tests/conftest.py — updated ASGI test fixtures to use the MongoDB repository with an in-memory test store.
- tests/test_auth.py — updated dotenv file target to .env_5aed5591dc897f4e.
- tests/test_games.py — updated dotenv file target to .env_5aed5591dc897f4e.
- tests/utils/factories.py — updated dotenv file target to .env_5aed5591dc897f4e.
- requirements.txt — replaced database dependencies with motor and pymongo.
- docker-compose.yml — replaced PostgreSQL service with MongoDB service and MongoDB environment variables.
- Dockerfile — updated exposed/runtime port to 39693.
- start.sh — updated startup port to 39693.
- README.md — documented MongoDB configuration and usage.
- .env.example — documented MongoDB environment variables.
- .env_93882a75-762a-45f3-a2b2-f23fdc62ca0d — updated legacy env content to MongoDB settings.

## Files Added
- .env_5aed5591dc897f4e — isolated environment file containing MongoDB settings and application secrets.
- pytest.ini — pytest asyncio configuration for generated/updated async tests.

## Secrets Extracted
- SECRET_KEY -> written to .env_5aed5591dc897f4e
- ALGORITHM -> written to .env_5aed5591dc897f4e
- ACCESS_TOKEN_EXPIRE_MINUTES -> written to .env_5aed5591dc897f4e

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5
- MongoDB configured as MONGO_URL=mongodb://localhost:27017 and MONGO_DATABASE=tic_tac_toe_imp

## Test Results Summary
- 10 PASSED, 0 FAILED, 0 SKIPPED
- python3 -m py_compile passed for modified Python files.
- FastAPI import check passed for app.main:app.
- Real uvicorn server boot verified on http://localhost:39693/health.
