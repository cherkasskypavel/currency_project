from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.api.schemas.user import UserInput, UserReturn
from app.db.database import get_session
from app.db.models import User
from app.core.security import hash_password


async def create_user(user: UserInput, session: AsyncSession):
    print("#" * 50)
    hashed_password = await hash_password(user.password)
    user_to_create = User(name=user.name,
                          email=user.email,
                          password=hashed_password)    
    session.add(user_to_create)
    await session.commit()
    await session.refresh(user_to_create)
    return user_to_create

