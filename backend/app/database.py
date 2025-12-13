import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Get DB URL from env or use default for local dev (though docker-compose handles this)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/pizzabot")

# Disable echo to avoid spamming logs, we will handle logging ourselves or rely on SQLModel/SQLAlchemy logs if needed
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
