# Pydantic schemas for authentication, games, and moves.
import uuid
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models import GameStatus, PlayerMark


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    username: str
    created_at: datetime


class GameCreate(BaseModel):
    pass


class GameUpdate(BaseModel):
    board: Optional[list[str]] = None
    current_player: Optional[PlayerMark] = None
    status: Optional[GameStatus] = None
    winner: Optional[PlayerMark] = None

    @field_validator("board")
    @classmethod
    def validate_board(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        if value is None:
            return value
        if len(value) != 9:
            raise ValueError("board must contain exactly 9 cells")
        if any(cell not in ("", "X", "O") for cell in value):
            raise ValueError("board cells must be '', 'X', or 'O'")
        return value


class ScoreboardCreate(BaseModel):
    pass


class ScoreboardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime


class MoveCreate(BaseModel):
    position: int = Field(ge=0, le=8)


class MoveRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    game_id: uuid.UUID
    player: PlayerMark
    position: int
    move_number: int
    created_at: datetime


class GameRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    board: list[str]
    current_player: PlayerMark
    status: GameStatus
    winner: Optional[PlayerMark]
    created_at: datetime
    updated_at: datetime
    moves: list[MoveRead] = []
