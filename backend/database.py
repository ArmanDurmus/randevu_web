from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.models.base import table_registry
from backend.settings import settings

engine = create_async_engine(settings.database_url)

def init_db():
    table_registry.metadata.create_all(bind=engine)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_session)] 