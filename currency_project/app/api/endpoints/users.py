from app.api.schemas.user import UserBase, UserInput
from app.api.schemas.token import Token
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import app.api.schemas as schemas
import app.db.crud as crud
import app.core.security as sec
from app.db.database import get_session

auth = APIRouter(prefix='/auth', tags=['auth'])


@auth.post('/register')
async def register_user(user: schemas.user.UserInput,
                        session: AsyncSession = Depends(get_session)):
    response = await crud.create_user(user, session)
    return {'message': f'Пользователь: {response.name}, id: {response.id}'}


@auth.post('/login', response_model = Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)):
    return await sec.authenticate_user(
        UserBase(email=form_data.username, password=form_data.password) 
        )

