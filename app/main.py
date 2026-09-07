# FastAPI application factory and top-level route registration.
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, games, scoreboards


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="tic-tac-toe-bknd",
    version="0.1.0",
    description="Simple FastAPI backend for a tic-tac-toe game.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(games.router, prefix=API_PREFIX)
app.include_router(scoreboards.router, prefix=API_PREFIX)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"name": "tic-tac-toe-bknd", "status": "ok"}
