import uuid
from datetime import datetime
from sqlalchemy import select, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from src.core.hash import verify_password
from src.utils import utcnow


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="author")

    @classmethod
    async def find_by_email(cls, db: AsyncSession, email: str):
        query = select(cls).where(cls.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def authenticate(cls, db: AsyncSession, email: str, password: str):
        user = await cls.find_by_email(db=db, email=email)
        if not user or not verify_password(password, user.password):
            return False
        return user
    
    @classmethod
    async def get_all_users(cls, db: AsyncSession):
        query = select(cls)
        result = await db.execute(query)
        return result.scalars().all()


class BlackListToken(Base):
    __tablename__ = "blacklisttokens"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    expire: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    author: Mapped["User"] = relationship(back_populates="tasks")

    @classmethod
    async def find_by_author(cls, db: AsyncSession, author: User):
        query = select(cls).where(cls.author_id == author.id)
        result = await db.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def find_by_id(cls, db: AsyncSession, task_id: uuid.UUID):
        query = select(cls).where(cls.id == task_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()