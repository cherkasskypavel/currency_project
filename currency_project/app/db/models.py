
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, MappedColumn, as_declarative, declared_attr

from app.api.schemas.user import UserReturn
from app.api.schemas.currency import CurrencyExternal



@as_declarative()
class BaseModel:

    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

  
class User(BaseModel):

    name: Mapped[str] = MappedColumn()
    email: Mapped[str] = MappedColumn()
    password: Mapped[str] = MappedColumn()

    @property
    def returnable(self):
        return UserReturn(
            id = self.id,
            name = self.name,
            email=self.email,
            password=self.password
        )
    
class Currency(BaseModel):

    code: Mapped[str] = MappedColumn()
    description: Mapped[str] = MappedColumn()

    @property
    def returnable(self):
        return CurrencyExternal(
            code=self.code,
            description=self.description    
        )
