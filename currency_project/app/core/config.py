from typing import Optional

from environs import Env
from dataclasses import dataclass
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    DB_ALEMBIC: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_DELTA: int
    API_KEY: str

    class Config:
        env_file = "currency_project/.env"

settings = Settings()
print(settings.DB_URL)
