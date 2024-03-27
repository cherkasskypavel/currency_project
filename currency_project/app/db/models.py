import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, MappedColumn, declared_attr

from app.api.schemas.user import UserReturn
from app.api.schemas.currency import CurrencyExternal
from app.db.database import Base


class User(Base):
    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)

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
    
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Currency(Base):
    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)
    code: Mapped[str] = MappedColumn()
    description: Mapped[str] = MappedColumn()

    @property
    def returnable(self):
        return CurrencyExternal(
            code=self.code,
            description=self.description    
        )

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class ExchangeRequest(Base):
    __tablename__ = "exchangerequest"

    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = MappedColumn(server_default=func.current_date())
    from_currency: Mapped[Optional[str]] = MappedColumn(ForeignKey("currency.code"))
    to_currency: Mapped[Optional[str]] = MappedColumn(ForeignKey("currency.code"))
    result: Mapped[float] = MappedColumn(nullable=False)


class ListRequest(Base):
    __tablename__ = "listrequest"

    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = MappedColumn(server_default=func.current_date())




    