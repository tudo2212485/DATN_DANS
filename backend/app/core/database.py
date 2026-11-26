import logging
from typing import AsyncGenerator, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import normalize_database_url, settings

logger = logging.getLogger("app.core.database")

POOL_PRE_PING = True
POOL_RECYCLE_SECONDS = 300

SYNC_DATABASE_URL = normalize_database_url(settings.DATABASE_URL, is_async=False)
ASYNC_DATABASE_URL = normalize_database_url(settings.DATABASE_URL_ASYNC, is_async=True)


def build_sync_engine(url: str):
    """Create sync SQLAlchemy engine with Neon-safe pooling & SSL normalization."""
    normalized_url = normalize_database_url(url, is_async=False)
    return create_engine(
        normalized_url,
        pool_pre_ping=POOL_PRE_PING,
        pool_recycle=POOL_RECYCLE_SECONDS,
        echo=False,
    )


def build_async_engine(url: str) -> Optional[AsyncEngine]:
    """Create async SQLAlchemy engine (asyncpg) with Neon-safe pooling & SSL normalization."""
    normalized_url = normalize_database_url(url, is_async=True)
    try:
        return create_async_engine(
            normalized_url,
            pool_pre_ping=POOL_PRE_PING,
            pool_recycle=POOL_RECYCLE_SECONDS,
            echo=False,
        )
    except ModuleNotFoundError as exc:
        logger.warning(f"Async DB driver unavailable for '{normalized_url.split('://')[0]}': {exc}")
        return None


# Engine kết nối SQLAlchemy (sync & async)
engine = build_sync_engine(SYNC_DATABASE_URL)
async_engine = build_async_engine(ASYNC_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = (
    async_sessionmaker(bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)
    if async_engine is not None
    else None
)

Base = declarative_base()


# Dependency cung cấp session cho FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("AsyncSessionLocal is not initialized (missing async database driver).")
    async with AsyncSessionLocal() as session:
        yield session
