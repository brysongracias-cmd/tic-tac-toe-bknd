COMMIT_MESSAGE: Add bot players and solo tic-tac-toe games

## Summary
- Added bot opponents that authenticated users can create.
- Users can start a solo game against a selected bot, make a move, and receive the bot's automatic response.
- Existing authentication and game behavior remains available.

## Features Added
- Added the Bot Player entity with a user-defined name.
- Added an authenticated operation to create a Bot Player.
- Added solo game creation linking a User, Game, and Bot Player.
- Added automatic Bot Player moves after each valid user move in a solo game.

## Files Modified
- app/core/auth.py — updated environment loading to use the project-specific environment file.
- app/core/security.py — moved the JWT secret fallback into the project environment file.
- app/database.py — reads the resolved database URL only from the project environment file.
- app/main.py — registered the Bot Player router and applies the solo-game column on existing databases.
- app/models.py — added BotPlayer and the optional Game relationship.
- app/routers/auth.py — updated environment loading.
- app/routers/games.py — added solo game creation and automatic bot turns.
- app/schemas.py — added Bot Player and solo game request/response fields.
- seed.py — updated environment loading.
- start.sh — honors the deployment PORT setting and starts without a development reloader.
- tests/conftest.py — updated environment loading.
- tests/test_auth.py — updated environment loading.
- tests/test_games.py — added coverage for Bot Player creation and solo play.
- tests/utils/factories.py — updated environment loading.

## Files Added
- app/routers/bot_players.py — authenticated Bot Player creation endpoint.

## Secrets Extracted
- SECRET_KEY -> written to .env_5aed5591dc897f4e.

## DB URLs Resolved
- postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5 -> postgresql+asyncpg://myuser:mypassword@localhost:5432/gen_ff84970ff5.

## Test Results Summary
- 11 PASSED, 0 FAILED, 0 SKIPPED.
- All project Python files passed compilation.
- The app entry point imported successfully.
