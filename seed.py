# Seed script that creates sample tic-tac-toe records in MongoDB.
import asyncio

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

from app.core.security import get_password_hash
from app.database import close_mongo_connection, connect_to_mongo, store
from app.models import PlayerMark


async def seed() -> None:
    await connect_to_mongo()
    try:
        if await store.find_user_by_email_or_username("alice@example.com") is None:
            users = []
            for username in ("alice", "bob", "carol"):
                users.append(await store.create_user(f"{username}@example.com", username, get_password_hash("password123")))
            for user in users:
                game = await store.create_game(user.id)
                game.board = ["X", "", "", "", "", "", "", "", ""]
                game.current_player = PlayerMark.O
                await store.add_move(game.id, PlayerMark.X, 0, 1)
                await store.update_game(game)
        users_count = len(store._users) if store.in_memory else await store.db.users.count_documents({})  # type: ignore[union-attr]
        games_count = len(store._games) if store.in_memory else await store.db.games.count_documents({})  # type: ignore[union-attr]
        print(f"Seed complete: {users_count} users, {games_count} games")
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(seed())
