# Seed script that creates database tables and sample tic-tac-toe records.
import asyncio

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash
from app.database import AsyncSessionLocal, Base, engine
from app.models import Game, Move, PlayerMark, User


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        users_result = await db.execute(select(User))
        if len(users_result.scalars().all()) == 0:
            users = [
                User(email="alice@example.com", username="alice", hashed_password=get_password_hash("password123")),
                User(email="bob@example.com", username="bob", hashed_password=get_password_hash("password123")),
                User(email="carol@example.com", username="carol", hashed_password=get_password_hash("password123")),
            ]
            db.add_all(users)
            await db.flush()
            for user in users:
                game = Game(owner_id=user.id)
                db.add(game)
                await db.flush()
                db.add(Move(game_id=game.id, player=PlayerMark.X, position=0, move_number=1))
                game.board = ["X", "", "", "", "", "", "", "", ""]
                game.current_player = PlayerMark.O
            await db.commit()
        games_result = await db.execute(select(Game).options(selectinload(Game.moves)))
        print(f"Seed complete: {len((await db.execute(select(User))).scalars().all())} users, {len(games_result.scalars().all())} games")


if __name__ == "__main__":
    asyncio.run(seed())
