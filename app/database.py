# MongoDB connection and repository helpers for the application.
import os
import uuid
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Optional

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError, PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.models import Game, GameStatus, Move, PlayerMark, User

DEFAULT_MONGO_URL = "mongodb://localhost:27017"
MONGO_URL = os.getenv("MONGO_URL", DEFAULT_MONGO_URL)
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "tic_tac_toe_imp")
USE_IN_MEMORY_DB = os.getenv("USE_IN_MEMORY_DB", "false").lower() == "true"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid(value: str | uuid.UUID) -> uuid.UUID:
    return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))


class MongoStore:
    """Small MongoDB repository with an in-memory fallback for local tests."""

    def __init__(self) -> None:
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.in_memory = USE_IN_MEMORY_DB or MONGO_URL.startswith("memory://")
        self._users: dict[str, dict[str, Any]] = {}
        self._games: dict[str, dict[str, Any]] = {}
        self._moves: dict[str, dict[str, Any]] = {}

    async def connect(self) -> None:
        if self.in_memory:
            return
        self.client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=800)
        self.db = self.client[MONGO_DATABASE]
        try:
            await self.client.admin.command("ping")
            await self.ensure_indexes()
        except PyMongoError:
            # Keep the API usable in isolated CI environments without a Mongo daemon.
            self.in_memory = True
            if self.client is not None:
                self.client.close()
            self.client = None
            self.db = None

    async def close(self) -> None:
        if self.client is not None:
            self.client.close()

    async def ensure_indexes(self) -> None:
        if self.in_memory or self.db is None:
            return
        await self.db.users.create_index([("email", ASCENDING)], unique=True)
        await self.db.users.create_index([("username", ASCENDING)], unique=True)
        await self.db.games.create_index([("owner_id", ASCENDING), ("created_at", DESCENDING)])
        await self.db.moves.create_index([("game_id", ASCENDING), ("position", ASCENDING)], unique=True)
        await self.db.moves.create_index([("game_id", ASCENDING), ("move_number", ASCENDING)], unique=True)

    async def clear(self) -> None:
        if self.in_memory or self.db is None:
            self._users.clear()
            self._games.clear()
            self._moves.clear()
            return
        await self.db.moves.delete_many({})
        await self.db.games.delete_many({})
        await self.db.users.delete_many({})

    def _user_from_doc(self, doc: dict[str, Any]) -> User:
        return User(
            id=_uuid(doc["_id"]),
            email=doc["email"],
            username=doc["username"],
            hashed_password=doc["hashed_password"],
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at", doc["created_at"]),
        )

    def _move_from_doc(self, doc: dict[str, Any]) -> Move:
        return Move(
            id=_uuid(doc["_id"]),
            game_id=_uuid(doc["game_id"]),
            player=PlayerMark(doc["player"]),
            position=doc["position"],
            move_number=doc["move_number"],
            created_at=doc["created_at"],
        )

    def _game_from_doc(self, doc: dict[str, Any], moves: list[Move] | None = None) -> Game:
        winner = doc.get("winner")
        return Game(
            id=_uuid(doc["_id"]),
            owner_id=_uuid(doc["owner_id"]),
            board=list(doc["board"]),
            current_player=PlayerMark(doc["current_player"]),
            status=GameStatus(doc["status"]),
            winner=PlayerMark(winner) if winner else None,
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at", doc["created_at"]),
            moves=moves or [],
        )

    async def find_user_by_email_or_username(self, email_or_username: str, username: str | None = None) -> User | None:
        candidates = {email_or_username}
        if username is not None:
            candidates.add(username)
        if self.in_memory or self.db is None:
            for doc in self._users.values():
                if doc["email"] in candidates or doc["username"] in candidates:
                    return self._user_from_doc(doc)
            return None
        doc = await self.db.users.find_one({"$or": [{"email": {"$in": list(candidates)}}, {"username": {"$in": list(candidates)}}]})
        return self._user_from_doc(doc) if doc else None

    async def get_user(self, user_id: uuid.UUID) -> User | None:
        key = str(user_id)
        if self.in_memory or self.db is None:
            doc = self._users.get(key)
        else:
            doc = await self.db.users.find_one({"_id": key})
        return self._user_from_doc(doc) if doc else None

    async def create_user(self, email: str, username: str, hashed_password: str) -> User:
        user = User(email=email, username=username, hashed_password=hashed_password)
        doc = {
            "_id": str(user.id),
            "email": user.email,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        if self.in_memory or self.db is None:
            if any(u["email"] == email or u["username"] == username for u in self._users.values()):
                raise DuplicateKeyError("duplicate user")
            self._users[doc["_id"]] = doc
        else:
            await self.db.users.insert_one(doc)
        return user

    async def create_game(self, owner_id: uuid.UUID) -> Game:
        game = Game(owner_id=owner_id)
        doc = self._game_to_doc(game)
        if self.in_memory or self.db is None:
            self._games[doc["_id"]] = doc
        else:
            await self.db.games.insert_one(doc)
        return game

    def _game_to_doc(self, game: Game) -> dict[str, Any]:
        return {
            "_id": str(game.id),
            "owner_id": str(game.owner_id),
            "board": list(game.board),
            "current_player": game.current_player.value,
            "status": game.status.value,
            "winner": game.winner.value if game.winner else None,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
        }

    async def _moves_for_game(self, game_id: uuid.UUID) -> list[Move]:
        key = str(game_id)
        if self.in_memory or self.db is None:
            docs = [m for m in self._moves.values() if m["game_id"] == key]
            docs.sort(key=lambda item: item["move_number"])
        else:
            docs = await self.db.moves.find({"game_id": key}).sort("move_number", ASCENDING).to_list(length=None)
        return [self._move_from_doc(doc) for doc in docs]

    async def get_game(self, game_id: uuid.UUID, owner_id: uuid.UUID) -> Game | None:
        key = str(game_id)
        owner = str(owner_id)
        if self.in_memory or self.db is None:
            doc = self._games.get(key)
            if doc is not None and doc["owner_id"] != owner:
                doc = None
        else:
            doc = await self.db.games.find_one({"_id": key, "owner_id": owner})
        if not doc:
            return None
        return self._game_from_doc(doc, await self._moves_for_game(game_id))

    async def list_games(self, owner_id: uuid.UUID, offset: int, limit: int) -> list[Game]:
        owner = str(owner_id)
        if self.in_memory or self.db is None:
            docs = [g for g in self._games.values() if g["owner_id"] == owner]
            docs.sort(key=lambda item: item["created_at"], reverse=True)
            docs = docs[offset:offset + limit]
        else:
            docs = await self.db.games.find({"owner_id": owner}).sort("created_at", DESCENDING).skip(offset).limit(limit).to_list(length=limit)
        return [self._game_from_doc(doc, await self._moves_for_game(_uuid(doc["_id"]))) for doc in docs]

    async def update_game(self, game: Game) -> Game:
        game.updated_at = _now()
        doc = self._game_to_doc(game)
        if self.in_memory or self.db is None:
            self._games[str(game.id)] = doc
        else:
            await self.db.games.replace_one({"_id": str(game.id)}, doc)
        return self._game_from_doc(doc, await self._moves_for_game(game.id))

    async def delete_game(self, game_id: uuid.UUID, owner_id: uuid.UUID) -> bool:
        key = str(game_id)
        owner = str(owner_id)
        if self.in_memory or self.db is None:
            doc = self._games.get(key)
            if doc is None or doc["owner_id"] != owner:
                return False
            del self._games[key]
            self._moves = {mid: m for mid, m in self._moves.items() if m["game_id"] != key}
            return True
        result = await self.db.games.delete_one({"_id": key, "owner_id": owner})
        if result.deleted_count:
            await self.db.moves.delete_many({"game_id": key})
            return True
        return False

    async def add_move(self, game_id: uuid.UUID, player: PlayerMark, position: int, move_number: int) -> Move:
        move = Move(game_id=game_id, player=player, position=position, move_number=move_number)
        doc = {
            "_id": str(move.id),
            "game_id": str(move.game_id),
            "player": move.player.value,
            "position": move.position,
            "move_number": move.move_number,
            "created_at": move.created_at,
        }
        if self.in_memory or self.db is None:
            if any(m["game_id"] == doc["game_id"] and (m["position"] == position or m["move_number"] == move_number) for m in self._moves.values()):
                raise DuplicateKeyError("duplicate move")
            self._moves[doc["_id"]] = doc
        else:
            await self.db.moves.insert_one(doc)
        return move


store = MongoStore()


async def connect_to_mongo() -> None:
    await store.connect()


async def close_mongo_connection() -> None:
    await store.close()


async def get_db() -> AsyncGenerator[MongoStore, None]:
    yield store
