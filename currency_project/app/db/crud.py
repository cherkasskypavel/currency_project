from typing import List
from datetime import date, datetime

from sqlalchemy import select, delete, insert, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

import app.api.schemas.currency as cur_sch
import app.api.schemas.user as user_sch
import app.core.security as sec
import app.db.models as md


async def create_user(user: user_sch.UserInput, session: AsyncSession):
    hashed_password = await sec.hash_password(user.password)
    user_to_create = md.User(name=user.name,
                          email=user.email,
                          password=hashed_password)    
    session.add(user_to_create)
    await session.commit()
    await session.refresh(user_to_create)
    return user_to_create.returnable 


async def get_currency_from_db(code: str,
                       session: AsyncSession):
    statement = select(md.Currency)\
        .where(md.Currency.code == code)
    db_currency = await session.execute(statement)
    return db_currency.scalar_one().returnable 


async def get_currencies_from_db(session: AsyncSession):
    statement = select(md.Currency).order_by(md.Currency.code)
    db_currency_list = await session.execute(statement)
    return [x.returnable for x in db_currency_list.scalars()]


async def update_currency_table(currencies: List[cur_sch.CurrencyExternal],
                                session: AsyncSession):
    delete_statement = delete(md.Currency)
    await session.execute(delete_statement)
    for x in currencies:
        insert_statement = insert(md.Currency)\
                           .values(**x.model_dump()) 
        await session.execute(insert_statement)

    await session.commit()
    return currencies


async def add_update_record(session: AsyncSession):
    new_record = md.ListRequest()
    session.add(new_record)
    await session.commit()
    await session.refresh(new_record)
    return new_record.id


async def get_latest_update(session: AsyncSession):
    stmt = select(md.ListRequest)\
            .order_by(desc(md.ListRequest.date))\
            .limit(1)

    result = await session.execute(stmt)
    last_update = result.scalar_one_or_none() 

    if last_update:
        return last_update.date
    else:
        return False
    

async def get_cached_exchange(exchange: cur_sch.CurrencyExchange,
                              session: AsyncSession) -> cur_sch.CurrencyExchangeResult:
    current_date = datetime.now().date()

    stmt = select(md.ExchangeRequest)\
        .where(and_(md.ExchangeRequest.from_currency == exchange.from_currency,
                    md.ExchangeRequest.to_currency == exchange.to_currency,
                    md.ExchangeRequest.date == current_date))\
        .limit(1)
    

    result = await session.execute(stmt)
    fresh_record = result.scalar_one_or_none()

    if fresh_record:
        total_result = fresh_record.result * exchange.amount
        exchange_to_return = cur_sch.CurrencyExchangeResult.model_validate(fresh_record)
        exchange_to_return.result = total_result
        exchange_to_return.amount = exchange.amount
        return exchange_to_return
    

async def add_exchange_request(exchange: cur_sch.CurrencyExchangeResult,
                                session: AsyncSession):

    new_record = md.ExchangeRequest(
        from_currency=exchange.from_currency,
        to_currency=exchange.to_currency,
        result=round(exchange.result / exchange.amount, 2)
    )

    session.add(new_record)
    await session.commit()
    await session.refresh(new_record)
    return new_record.id

    
