# Scoreboard API routes.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.database import get_db
from app.models import Scoreboard, User
from app.schemas import ScoreboardCreate, ScoreboardRead

router = APIRouter(prefix="/scoreboards", tags=["scoreboards"])


@router.post("/", response_model=ScoreboardRead, status_code=status.HTTP_201_CREATED)
async def create_scoreboard(
    payload: ScoreboardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Scoreboard:
    scoreboard = Scoreboard(owner_id=current_user.id, score=payload.score)
    db.add(scoreboard)
    await db.commit()
    await db.refresh(scoreboard)
    return scoreboard
