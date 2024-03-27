from typing import List
from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
import app.utils.external_api as ea
import app.db.crud as crud
import app.core.security as sec
import app.api.schemas.currency as cur_sch
import app.api.schemas.user as user_sch


currency = APIRouter(prefix='/currency',
                     tags=['currency'])


@currency.get('/list')
async def get_currency_list(user: user_sch.UserFromToken = Depends(sec.get_user_from_token),
                            session: AsyncSession = Depends(get_session)): 

    latest_update = await crud.get_latest_update(session)
    if not latest_update or latest_update < date.today():
        fresh_currencies = await ea.get_currencies_from_API()
        await crud.update_currency_table(fresh_currencies, session)
        await crud.add_update_record(session)
        return fresh_currencies
    else: 
        result = await crud.get_currencies_from_db(session=session)
        return result
            

@currency.get('/exchange')
async def get_exchange(from_currency: str, to_currency: str, amount: float=1.0,
                       user: user_sch.UserFromToken = Depends(sec.get_user_from_token),
                       session: AsyncSession = Depends(get_session)):
    
    from_cur = from_currency.upper()
    to_cur = to_currency.upper()

    currencies_in_db = set(map(lambda x: x.code, await crud.get_currencies_from_db(session)))

    if not currencies_in_db.issuperset((from_cur, to_cur)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Такие валюты не найдены.")
    
    exchange = cur_sch.CurrencyExchange(from_currency=from_cur,
                                to_currency=to_cur,
                                amount=amount)

    cached_exchange = await crud.get_cached_exchange(exchange, session)
    
    if cached_exchange:
        return cached_exchange
    
    external_api_exchange = await ea.exchange_currency(
            cur_sch.CurrencyExchange(from_currency=from_cur,
                                to_currency=to_cur,
                                amount=amount)
                                        )
    success_db_adding = await crud.add_exchange_request(external_api_exchange, session)
    
    if success_db_adding:
        return external_api_exchange
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Проблема с базой данных на сервере.")
    