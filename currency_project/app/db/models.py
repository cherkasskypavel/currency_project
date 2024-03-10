from typing import Optional

from sqlalchemy.orm import Mapped, MappedColumn, as_declarative, declared_attr

from app.api.schemas.user import UserReturn
from app.db.database import Base

@as_declarative()
class BaseModel:

    id: Mapped[int] = MappedColumn(primary_key=True, autoincrement=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class User(BaseModel):

    __tablename__ = 'user'

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