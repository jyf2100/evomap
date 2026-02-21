"""Database configuration and session management."""
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models import Base  # Re-export for convenience

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Initialize database connection."""
    async with engine.begin() as conn:
        # Test connection
        await conn.execute(text("SELECT 1"))


async def get_session() -> AsyncSession:
    """Get database session dependency."""
    async with async_session() as session:
        yield session
