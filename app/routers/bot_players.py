# Bot player creation API route.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.database import get_db
from app.models import BotPlayer, User
from app.schemas import BotPlayerCreate, BotPlayerRead

router = APIRouter(prefix="/bot-players", tags=["bot players"])


@router.post("/", response_model=BotPlayerRead, status_code=status.HTTP_201_CREATED)
async def add_bot_player(
    payload: BotPlayerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BotPlayer:
    existing = await db.execute(select(BotPlayer).where(BotPlayer.name == payload.name))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bot player name already exists")

    bot_player = BotPlayer(name=payload.name)
    db.add(bot_player)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bot player name already exists") from None
    await db.refresh(bot_player)
    return bot_player
