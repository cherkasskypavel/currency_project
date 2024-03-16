from typing import List

from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserInput
from app.api.schemas.currency import CurrencyExternal
import app.core.security as sec
import app.db.models as md


async def create_user(user: UserInput, session: AsyncSession):
    print("#" * 50)
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


async def update_currency_table(currencies: List[CurrencyExternal],
                                session: AsyncSession):
    delete_statement = delete(md.Currency)
    await session.execute(delete_statement)
    for x in currencies:
        insert_statement = insert(md.Currency)\
                           .values(**x.model_dump()) 
        await session.execute(insert_statement)

    await session.commit()
    session.close()

    return currencies