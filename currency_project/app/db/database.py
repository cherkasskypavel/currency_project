

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.core.config import settings


engine = create_async_engine(
    url = settings.DB_URL,
    echo=True,
    future=True,
    connect_args={
        'check_same_thread': False
    }
)

class Base(DeclarativeBase):
    pass

session_maker = async_sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   autoflush=False)

async def get_session():
    async with session_maker() as async_session:
        yield async_session

