import string

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserBase(BaseModel):
    email: str = Field(pattern=r"\w+@[a-z]+\.[a-z]{2, 3}", default='')
    password: str = Field(default='')

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not (
            len(value) >= 8 and
            set(value).intersection(string.ascii_uppercase) and
            set(value).intersection(string.ascii_lowercase) and
            set(value).intersection(string.digits) and
            set(value).intersection(string.punctuation)
        ):
            raise ValueError("Пароль не соответствует следующим критериям:\n"
                             "1. Должен содержать 8 или более символов\n"
                             "2. Должен содержать хотябы одну заглавную букву\n"
                             "3. Должен содержать хотябы одну прописную букву\n"
                             "4. Должен содержать хотябы одну цифру\n"
                             "5. Должен содержать хотябы один символ пунктуации\n")
        else:
            return value

    class Config:
        orm_mode = True

class UserInput(UserBase):
    name: str = Field(default='')


class UserReturn(UserInput):
    model_config = ConfigDict(from_attributes=True)
    id: int

class UserFromToken(BaseModel):
    id: int
    username: str

