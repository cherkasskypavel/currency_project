import aiohttp

from app.api.schemas.currency import CurrencyExternal
from app.api.schemas.currency import CurrencyExchange
from app.api.schemas.currency import CurrencyExchangeResult
from app.core.config import settings



async def get_currencies_from_API():
    headers = {'apiKey': settings.API_KEY}

    async with aiohttp.ClientSession(base_url=settings.EXTERNAL_API_URL,
                                     headers=headers) as session:
        async with session.get('/currency_data/list') as response:
            response.raise_for_status()
            currency_list = await response.json()
            validated = list(CurrencyExternal(code=k, description=v) for k, v in dict(currency_list.items())['currencies'].items())
            return validated


async def exchange_currency(exchange_form: CurrencyExchange) -> CurrencyExchangeResult:
    params = {
        'to': exchange_form.to_currency,
        'from': exchange_form.from_currency,
        'amount': exchange_form.amount
    }
    headers = {'apiKey': settings.API_KEY}
    
    
    async with aiohttp.ClientSession(base_url=settings.EXTERNAL_API_URL,
                                      headers=headers) as session:
        async with session.get('/currency_data/convert', params=params) as response:
            response.raise_for_status()
            result = await response.json()
            return CurrencyExchangeResult(**exchange_form.model_dump(),
                                          result=result['result'])
            