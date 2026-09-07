COMMIT_MESSAGE: Add scoreboard creation endpoint

## Features Added
- Added the Scoreboard entity with generated identifier and creation timestamp.
- Added `POST /api/v1/scoreboards/` to create a scoreboard and return it with HTTP 201.

## Files Modified
- app/main.py — registered the scoreboard router and standardized dotenv loading.
- app/models.py — added the Scoreboard SQLAlchemy model and standardized dotenv loading.
- app/schemas.py — added request and response schemas for scoreboard creation.
- app/database.py — loads the job-specific environment file and requires the configured database URL.
- app/core/security.py — loads the job-specific environment file and requires the configured secret key.
- app/core/auth.py, app/routers/auth.py, app/routers/games.py, seed.py, tests/, and existing report scripts — standardized dotenv loading to `.env_5aed5591dc897f4e`.

## Files Added
- app/routers/scoreboards.py — scoreboard creation route.
- .env_5aed5591dc897f4e — job-specific application configuration, database URL, and authentication secret.

## Secrets Extracted
- SECRET_KEY -> written to .env_5aed5591dc897f4e

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5
- postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5

## Test Results Summary
- 21 PASSED, 10 FAILED, 0 SKIPPED
- All 21 Python files completed compilation and the `app.main` import check passed.
- The 10 existing database-backed pytest cases could not run because PostgreSQL is unavailable at localhost:5432 in this environment; each fails during fixture setup before endpoint execution.
