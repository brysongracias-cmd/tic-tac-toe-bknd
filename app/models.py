# Domain models for users, tic-tac-toe games, and moves stored in MongoDB.
import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PlayerMark(str, enum.Enum):
    X = "X"
    O = "O"


class GameStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


@dataclass
class User:
    email: str
    username: str
    hashed_password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)


@dataclass
class Move:
    game_id: uuid.UUID
    player: PlayerMark
    position: int
    move_number: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Game:
    owner_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    board: list[str] = field(default_factory=lambda: ["", "", "", "", "", "", "", "", ""])
    current_player: PlayerMark = PlayerMark.X
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[PlayerMark] = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    moves: list[Move] = field(default_factory=list)
