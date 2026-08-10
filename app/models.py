# SQLAlchemy ORM models for users, tic-tac-toe games, and moves.
import enum
import uuid
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv('.env_93882a75-762a-45f3-a2b2-f23fdc62ca0d', override=True)
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PlayerMark(str, enum.Enum):
    X = "X"
    O = "O"


class GameStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    games: Mapped[List["Game"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    board: Mapped[list[str]] = mapped_column(JSONB, default=lambda: ["", "", "", "", "", "", "", "", ""], nullable=False)
    current_player: Mapped[PlayerMark] = mapped_column(Enum(PlayerMark, name="player_mark"), default=PlayerMark.X, nullable=False)
    status: Mapped[GameStatus] = mapped_column(Enum(GameStatus, name="game_status"), default=GameStatus.IN_PROGRESS, nullable=False)
    winner: Mapped[Optional[PlayerMark]] = mapped_column(Enum(PlayerMark, name="winner_mark"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped[User] = relationship(back_populates="games")
    moves: Mapped[List["Move"]] = relationship(back_populates="game", cascade="all, delete-orphan", order_by="Move.move_number")


class Move(Base):
    __tablename__ = "moves"
    __table_args__ = (
        UniqueConstraint("game_id", "position", name="uq_move_game_position"),
        UniqueConstraint("game_id", "move_number", name="uq_move_game_number"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    player: Mapped[PlayerMark] = mapped_column(Enum(PlayerMark, name="move_player_mark"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    move_number: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    game: Mapped[Game] = relationship(back_populates="moves")
