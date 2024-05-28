from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import Config

DATABASE_URL = Config.DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


celery_engine = create_engine(DATABASE_URL, echo=True)
CelerySession = sessionmaker(bind=celery_engine)
celery_session = CelerySession()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
