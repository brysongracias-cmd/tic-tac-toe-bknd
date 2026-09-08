COMMIT_MESSAGE: Add scoreboard creation endpoint

## Features Added
- Added the Scoreboard entity with a generated identifier and creation timestamp.
- Added `POST /api/v1/scoreboards/` to create a scoreboard and return it with HTTP 201.

## Files Modified
- app/main.py — registered the scoreboard router and standardized dotenv loading.
- app/models.py — added the Scoreboard SQLAlchemy model.
- app/schemas.py — added request and response schemas for scoreboard creation.
- app/database.py — loads the job-specific environment file and requires the configured database URL.
- app/core/security.py — loads the job-specific environment file and requires the configured secret key.
- .env_5aed5591dc897f4e — configured the required default port.

## Files Added
- app/routers/scoreboards.py — scoreboard creation route.
- tests/test_scoreboards.py — coverage for scoreboard creation.

## Secrets Extracted
- SECRET_KEY -> written to .env_5aed5591dc897f4e
- DATABASE_URL -> written to .env_5aed5591dc897f4e

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5
- postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@db:5432/gen_ff84970ff5

## Test Results Summary
- 21 PASSED, 11 FAILED, 0 SKIPPED
- All 21 Python files completed syntax compilation and the `app.main` import check passed.
- The 11 database-backed pytest cases could not run because PostgreSQL is unavailable at localhost:5432; each failed during fixture setup before endpoint execution.
