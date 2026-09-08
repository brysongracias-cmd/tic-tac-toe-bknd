# Scoreboard creation API route.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Scoreboard
from app.schemas import ScoreboardCreate, ScoreboardRead

router = APIRouter(prefix="/scoreboards", tags=["scoreboards"])


@router.post("/", response_model=ScoreboardRead, status_code=status.HTTP_201_CREATED)
async def create_scoreboard(
    _: ScoreboardCreate,
    db: AsyncSession = Depends(get_db),
) -> Scoreboard:
    scoreboard = Scoreboard()
    db.add(scoreboard)
    await db.commit()
    await db.refresh(scoreboard)
    return scoreboard
