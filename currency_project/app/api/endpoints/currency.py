from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.schemas.currency import CurrencyExchange
from app.api.schemas.currency import CurrencyExternal
from app.api.schemas.currency import CurrencyTypeBase
from app.api.schemas.user import UserFromToken
from app.core.security import get_user_from_token, get_user_by_id
from app.db.database import get_session
from app.utils.external_api import exchange_currency, get_currencies_from_API
from app.db.crud import get_currencies_from_db, get_currency_from_db, update_currency_table

currency = APIRouter(prefix='/currency',
                     tags=['currency'])


@currency.get('/list')
async def get_currency_list(user: UserFromToken = Depends(get_user_from_token),
                            session: AsyncSession = Depends(get_session)):
    
    fresh_currencies = await get_currencies_from_API()
    await update_currency_table(fresh_currencies, session)
    return fresh_currencies


@currency.get('/exchange')
async def get_exchange(from_cur:str, to_cur:str, amount: float=1.0,
                       user: UserFromToken = Depends(get_user_from_token),
                       session: AsyncSession = Depends(get_session)):
    

    user_in_db = await get_user_by_id(user.id, session)


    if user_in_db:
        from_cur = from_cur.upper()
        to_cur = to_cur.upper()
        cur1_in_db = await get_currency_from_db(from_cur, session)
        cur2_in_db = await get_currency_from_db(to_cur, session)
        if cur1_in_db and cur2_in_db:
            result = await exchange_currency(
                CurrencyExchange(from_currency=from_cur,
                                  to_currency=to_cur,
                                    amount=amount)
                                            )
            return result
        # raise HTTP
    #raise HTTP
        
    
    # если получаем ошибку
    # некорректного кода
    # то обнвляем таблицу 
    # валютами
     