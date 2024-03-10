

from app.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import status
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserBase, UserFromToken, UserInput, UserReturn  
from app.db.database import get_session

crypt_context = CryptContext(['bcrypt'])
oauth2scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)) -> UserReturn:
    statement = select(User).where(User.email == email)
    result = session.execute(statement)
    return result.returnable()


async def validate_user(current_password, to_compare):
    return crypt_context.verify(current_password, to_compare)


async def hash_password(password: str):
    return crypt_context.hash(password)

#######################################################################
async def generate_jwt(user: UserReturn):
    token_data = {
        'exp': settings.JWT_EXPIRE_DELTA, # подключить файл конфигурации
        'id': settings.id,
        'username': settings.name
    }
    algorithm = settings.JWT_ALGORITHM # подключить файл конфигурации
    key = settings.JWT_SECRET_KEY # подключить файл конфигурации
    return jwt.encode(token_data, algorithm=algorithm, key=key)




async def authenticate_user(user: UserBase):

    user_in_db = await get_user_by_email(user.email)
    if user_in_db:
        if validate_user(user.password, user_in_db.password):
            return generate_jwt(user_in_db)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Ошибка аутентификации!')

#######################################################################

async def decode_token(token):
    payload = jwt.decode(token=token,
                         algorithms=[config.JWT_ALGORITHM],
                         key=settings.JWT_SECRET_KEY) # подключить config
    return payload

async def get_user_from_token(token: str = Depends(oauth2scheme)):
    try:
        payload = await decode_token(token)
        return UserFromToken(**payload)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Токен недействителен!') 
