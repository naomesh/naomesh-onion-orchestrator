from sqlalchemy import Column, MetaData
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
    start_time = Column(Integer)
    end_time = Column(Integer)
    pictures_quantity = Column(Integer)


async def insert_result(res: Result):
    _, async_session = get_engine()
    async with async_session() as session:  # type: ignore
        async with session.begin():
            await session.add_all(res)
            await session.commit()


async def push_schema():
    # engine is an instance of AsyncEngine
    (engine, _) = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all, checkfirst=True)
