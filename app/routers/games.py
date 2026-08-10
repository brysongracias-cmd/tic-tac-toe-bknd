# Tic-tac-toe game API routes and move application logic.
import uuid
from typing import Sequence

from dotenv import load_dotenv
load_dotenv('.env_93882a75-762a-45f3-a2b2-f23fdc62ca0d', override=True)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth import get_current_user
from app.database import get_db
from app.models import Game, GameStatus, Move, PlayerMark, User
from app.schemas import GameCreate, GameRead, GameUpdate, MoveCreate

router = APIRouter(prefix="/games", tags=["games"])

WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def evaluate_board(board: Sequence[str]) -> tuple[GameStatus, PlayerMark | None]:
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            winner = PlayerMark(board[a])
            return (GameStatus.X_WON if winner == PlayerMark.X else GameStatus.O_WON, winner)
    if all(board):
        return GameStatus.DRAW, None
    return GameStatus.IN_PROGRESS, None


async def get_owned_game(game_id: uuid.UUID, current_user: User, db: AsyncSession) -> Game:
    result = await db.execute(
        select(Game).options(selectinload(Game.moves)).where(Game.id == game_id, Game.owner_id == current_user.id)
    )
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return game


@router.post("/", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def create_game(_: GameCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Game:
    game = Game(owner_id=current_user.id)
    db.add(game)
    await db.commit()
    result = await db.execute(select(Game).options(selectinload(Game.moves)).where(Game.id == game.id))
    return result.scalar_one()


@router.get("/", response_model=list[GameRead])
async def list_games(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[Game]:
    result = await db.execute(
        select(Game)
        .options(selectinload(Game.moves))
        .where(Game.owner_id == current_user.id)
        .order_by(Game.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all())


@router.get("/{game_id}", response_model=GameRead)
async def get_game(game_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Game:
    return await get_owned_game(game_id, current_user, db)


@router.patch("/{game_id}", response_model=GameRead)
async def update_game(
    game_id: uuid.UUID,
    payload: GameUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = await get_owned_game(game_id, current_user, db)
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(game, key, value)
    await db.commit()
    result = await db.execute(select(Game).options(selectinload(Game.moves)).where(Game.id == game.id))
    return result.scalar_one()


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    game = await get_owned_game(game_id, current_user, db)
    await db.delete(game)
    await db.commit()
    return None


@router.post("/{game_id}/moves", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def make_move(
    game_id: uuid.UUID,
    payload: MoveCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Game:
    game = await get_owned_game(game_id, current_user, db)
    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Game is already complete")
    board = list(game.board)
    if board[payload.position] != "":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cell is already occupied")
    player = game.current_player
    board[payload.position] = player.value
    game.board = board
    new_status, winner = evaluate_board(board)
    game.status = new_status
    game.winner = winner
    if new_status == GameStatus.IN_PROGRESS:
        game.current_player = PlayerMark.O if player == PlayerMark.X else PlayerMark.X
    move = Move(game_id=game.id, player=player, position=payload.position, move_number=len(game.moves) + 1)
    game.moves.append(move)
    await db.commit()
    result = await db.execute(
        select(Game).options(selectinload(Game.moves)).where(Game.id == game.id).execution_options(populate_existing=True)
    )
    return result.scalar_one()
