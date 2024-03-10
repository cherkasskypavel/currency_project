from pydantic import BaseModel


class Token(BaseModel):
    acces_token: str
    token_type: str


