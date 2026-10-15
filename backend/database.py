from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.models.base import table_registry

#Later change the url
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL)

def init_db():
    table_registry.metadata.create_all(bind=engine)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

DBSession = Annotated[AsyncSession, get_session()] 