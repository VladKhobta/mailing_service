from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

engine = create_async_engine(
    settings.REAL_DATABASE_URL,
    future=True,
    echo=False,
    execution_options={
        "isolation_level": "AUTOCOMMIT"
    },
)

# noinspection PyTypeChecker
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=True,
    class_=AsyncSession
)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
