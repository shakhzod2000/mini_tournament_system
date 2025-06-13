from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.config import settings

Base = declarative_base()

# Async engine (used by FastAPI app)
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Sync engine (used by Alembic)
sync_engine = create_engine(settings.SYNC_DATABASE_URL, echo=True)
