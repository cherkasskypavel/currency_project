from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

class UserInput(UserBase):
    name: str


class UserReturn(UserInput):
    model_config = ConfigDict(from_attributes=True)
    id: int

class UserFromToken(BaseModel):
    id: int
    username: str

