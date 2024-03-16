from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, validator, ConfigDict


class CurrencyTypeBase(BaseModel):
    code: str = Field(pattern=r"[A-Z]{3}")

    class Config:
        orm_mode: True
        
class CurrencyExternal(CurrencyTypeBase):
    model_config = ConfigDict(from_attributes=True)
    description: Optional[str]


class CurrencyList(BaseModel):
    Currencies: List[CurrencyExternal] 

    class Config:
        orm_mode = True


class CurrencyExchange(BaseModel): 
    from_currency: str  
    to_currency: str  
    amount: float = 1.0


class CurrencyExchangeResult(CurrencyExchange):
    result: float

    @validator('result')
    def result_check(cls, v):
        ...
        return round(v, 2)
