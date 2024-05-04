from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class UserRoom(Base):
    __tablename__ = "user_room"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(Integer())
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5433/query"
)
Base.metadata.create_all(bind=engine)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
