import asyncio
import os
import os.path
from pathlib import Path

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
import pytest as pt

from app.db.database import Base
from main import app
from app.db.database import get_session
from app.core.config import settings
import app.api.schemas.currency as scc
import app.api.schemas.user as scu
import app.api.schemas.token as sct
import app.db.models as md



_test_engine = create_async_engine(
    url=settings.TEST_DB_URL,
    echo=True,
    future=True,
    connect_args={
        'check_same_thread': False
    }
)



_test_session_maker = async_sessionmaker(bind=_test_engine,
                                         class_=AsyncSession,
                                         autoflush=False)

async def _test_get_session():
    async with _test_session_maker() as async_session:
        yield async_session

app.dependency_overrides[get_session] = _test_get_session



async def create_models():
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



def clear_test_db(db_ref: str = settings.TEST_DB_PATH):
    pwd = Path.cwd()
    db_abs = Path.joinpath(pwd, db_ref)
    if db_abs.is_file():
        db_abs.unlink()
