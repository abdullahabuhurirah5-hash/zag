from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.base import metadata


async def init_db() -> None:
    """Create database tables from metadata."""
    engine = create_async_engine(settings.POSTGRES_URI)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
