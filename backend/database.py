from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.models.base import table_registry
from backend.settings import settings

engine = create_async_engine(settings.database_url)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(
            table_registry.metadata.create_all
        )

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_session)] 