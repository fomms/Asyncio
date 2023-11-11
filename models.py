from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


PG_DSN = f'postgresql+asyncpg://app:1234@127.0.0.1:5431/app'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class People(Base):
    __tablename__ = 'SWAPI'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(500))
    eye_color: Mapped[str] = mapped_column(String(500))
    films: Mapped[str] = mapped_column(String(500))
    gender: Mapped[str] = mapped_column(String(500))
    hair_color: Mapped[str] = mapped_column(String(500))
    height: Mapped[str] = mapped_column(String(500))
    homeworld: Mapped[str] = mapped_column(String(500))
    mass: Mapped[str] = mapped_column(String(500))
    name: Mapped[str] = mapped_column(String(500))
    skin_color: Mapped[str] = mapped_column(String(500))
    species: Mapped[str] = mapped_column(String(500))
    starships: Mapped[str] = mapped_column(String(500))
    vehicles: Mapped[str] = mapped_column(String(500))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
