from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import env


def get_engine():
    engine = create_async_engine(
        env("PREFECT_ORION_DATABASE_CONNECTION_URL"),
        echo=False,
    )
    return engine, sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
