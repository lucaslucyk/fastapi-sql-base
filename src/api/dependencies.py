from typing import Any, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session


async def get_db() -> Generator[AsyncSession, Any, None]:
    """ Get Async db session generator with aiosqlite engine.

    Yields:
        Generator: Async session generated with async engine and AsyncSession
    """
    async with async_session() as db_session:
        yield db_session