from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    url=settings.database.uri,
    **settings.DATABASE.engine_kwargs,
)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Return async session with already set commits, rollbacks, closes."""

    async_session: AsyncSession = async_session_factory()
    try:
        yield async_session
        await async_session.commit()
    except BaseException as e:
        await async_session.rollback()
        raise e from None
    finally:
        await async_session.close()
