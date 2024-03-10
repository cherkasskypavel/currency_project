from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str

class UserInput(UserBase):
    name: str


class UserReturn(UserInput):
    id: int

class UserFromToken(BaseModel):
    id: int
    username: str