COMMIT_MESSAGE: Add authenticated scoreboard creation

## Features Added
- Added the Scoreboard entity with an authenticated score submission operation at `POST /api/v1/scoreboards/`.
- Added request and response schemas for scoreboard score submissions.

## Files Modified
- app/main.py — registered the scoreboard router and switched application configuration loading to the required environment file.
- app/models.py — added Scoreboard persistence and its owner relationship.
- app/schemas.py — added ScoreboardCreate and ScoreboardRead schemas.
- app/database.py — loads the required environment file and reads the database URL from it.
- app/core/security.py — loads the required environment file and reads the signing key from it.
- tests/conftest.py — loads the required environment file for database-aware tests.
- .env_5aed5591dc897f4e — set the required default port.

## Files Added
- app/routers/scoreboards.py — authenticated scoreboard creation endpoint.
- tests/test_scoreboards.py — coverage for scoreboard creation.

## Secrets Extracted
- SECRET_KEY -> written to .env_5aed5591dc897f4e
- DATABASE_URL -> written to .env_5aed5591dc897f4e

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5

## Test Results Summary
- 0 PASSED, 0 FAILED, 11 SKIPPED
- All pytest endpoint tests were skipped by the unavailable local PostgreSQL service: connections to localhost:5432 were refused. Python syntax compilation and application import checks passed.
