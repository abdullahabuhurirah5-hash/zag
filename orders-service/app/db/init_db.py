from app.db.session import engine


async def init_db() -> None:
    # simple convenience for dev: create tables
    from app.db.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
