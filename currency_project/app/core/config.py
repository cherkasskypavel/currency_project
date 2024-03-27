from typing import Optional

from environs import Env
from dataclasses import dataclass
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DIALECT_DRIVER: str
    DB_PATH: str
    TEST_DB_PATH: str
    DB_ALEMBIC: str
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_EXPIRE_DELTA: int
    API_KEY: str
    EXTERNAL_API_URL: str

    @property
    def DB_URL(self):
        return self.DIALECT_DRIVER + self.DB_PATH
    
    @property
    def TEST_DB_URL(self):
        return self.DIALECT_DRIVER + self.TEST_DB_PATH

    class Config:
        env_file = "currency_project/.env"

settings = Settings()
print(settings.DB_URL)
