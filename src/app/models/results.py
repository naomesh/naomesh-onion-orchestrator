from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, DateTime, MetaData, delete
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

from app.models.connection import get_engine

Base = declarative_base()
metadata_obj = MetaData()


class Result(Base):
    __tablename__ = "results"
    metadata = metadata_obj
    job_id = Column(String(), primary_key=True)
    total_consumption_kwh = Column(Integer)
    model_obj_key = Column(String())
    texture_obj_key = Column(String())
    total_production_kwh = Column(Integer)
    node_id = Column(String())
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    pictures_quantity = Column(Integer)


async def insert_or_update(dbsession: AsyncSession, res: Result):
    """Replaces the the column last_event_at for a named pair."""
    q = delete(Result).where(Result.job_id == res.job_id)
    await dbsession.execute(q)
    await dbsession.commit()
    async with dbsession.begin():
        dbsession.add_all([res])
    await dbsession.commit()


async def insert_result(res: Result):
    _, async_session = get_engine()
    async with async_session() as session:  # type: ignore
        await insert_or_update(session, res)
        await session.commit()


async def push_schema():
    # engine is an instance of AsyncEngine
    (engine, _) = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all, checkfirst=True)
