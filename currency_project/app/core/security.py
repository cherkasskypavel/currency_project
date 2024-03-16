from datetime import datetime, timedelta

from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserBase, UserFromToken, UserReturn  
import app.db.models as md


crypt_context = CryptContext(['bcrypt'])
oauth2scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_user_by_id(id: int, 
                            session: AsyncSession) -> UserReturn:
    statement = select(md.User).where(md.User.id == id)
    result = await session.execute(statement)
    return result.scalar_one().returnable


async def get_user_by_email(email: str, 
                            session: AsyncSession) -> UserReturn:
    statement = select(md.User).where(md.User.email == email)
    result = await session.execute(statement)
    return result.scalar_one().returnable


def validate_user(current_password, to_compare):
    return crypt_context.verify(current_password, to_compare)


async def hash_password(password: str):
    return crypt_context.hash(password)


def generate_jwt(user: UserReturn):
    token_data = {
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_DELTA),
        'id': user.id,
        'username': user.name
    }
    algorithm = settings.JWT_ALGORITHM 
    key = settings.JWT_SECRET_KEY 
    print('PRINT FROM GENERATE_JWT')
    return jwt.encode(token_data, algorithm=algorithm, key=key)


async def authenticate_user(user: UserBase,
                            session: AsyncSession):

    user_in_db = await get_user_by_email(user.email, session)
    if user_in_db:
        if validate_user(user.password, user_in_db.password):
            return user_in_db 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Ошибка аутентификации!')


def decode_token(token):
    payload = jwt.decode(token=token,
                         algorithms=[settings.JWT_ALGORITHM],
                         key=settings.JWT_SECRET_KEY)
    return payload


def get_user_from_token(token: str = Depends(oauth2scheme)):
    try:
        payload = decode_token(token)
        return UserFromToken(**payload)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Токен недействителен!') 
