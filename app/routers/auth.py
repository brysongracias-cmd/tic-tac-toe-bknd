# Authentication API routes for registration, login, and current-user lookup.
from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError

from app.core.auth import get_current_user
from app.core.security import create_access_token, get_password_hash, verify_password
from app.database import MongoStore, get_db
from app.models import User
from app.schemas import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: MongoStore = Depends(get_db)) -> User:
    existing = await db.find_user_by_email_or_username(str(payload.email), payload.username)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists")
    try:
        return await db.create_user(str(payload.email), payload.username, get_password_hash(payload.password))
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already exists") from None


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: MongoStore = Depends(get_db)) -> Token:
    user = await db.find_user_by_email_or_username(form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
