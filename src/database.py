from typing import Any, Optional
from fastapi import HTTPException, status
from pydantic import PostgresDsn
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from .core import config

PG_URL = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=str(config.POSTGRES_PORT),
    database=config.POSTGRES_DB,
)

engine = create_async_engine(PG_URL, future=True, echo=True)
SessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    async def save(self, db: AsyncSession) -> None:
        """
        Save the current instance to the database.
        
        :param db: AsyncSession
        :return: None
        """
        try:
            db.add(self)
            await db.commit()
        except SQLAlchemyError as ex:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    @classmethod
    async def find_by_id(cls, db: AsyncSession, id: str) -> Optional["Base"]:
        """
        Find an instance by its ID.
        
        :param db: AsyncSession
        :param id: ID of the instance
        :return: The instance if found, otherwise None
        """
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalars().first()
