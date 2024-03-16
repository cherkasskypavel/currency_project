
from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserBase, UserInput
from app.api.schemas.token import Token
import app.core.security as sec
import app.db.crud as crud
from app.db.database import get_session

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/register')
async def register_user(user: UserInput,
                        session: AsyncSession = Depends(get_session)):
    try:
        user_in_db = await sec.get_user_by_email(user.email, session)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User {user.name} already exists!')
    except NoResultFound:
        ...
        
    response = await crud.create_user(user, session)
    return {'message': f'Пользователь: {response.name}, id: {response.id}'}


@auth.post('/login', response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)):
    user_in_db = await sec.authenticate_user(
        UserBase(email=form_data.username, password=form_data.password),
        session 
        )
    if user_in_db:
        token = sec.generate_jwt(user_in_db)
    print(token, '<-----------------------------------------------token')
    return {'access_token': token, 'token_type': 'bearer'}
