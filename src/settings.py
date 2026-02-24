from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import SecretStr

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: SecretStr = SecretStr("supersecretkey123")

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_DB: str = "coursebackend"

    REDIS_URL: str = "redis://localhost:6379"

    def get_database_url(self, use_async: bool = True):
        driver = "postgresql+asyncpg" if use_async else "postgresql"
        return f"{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_redis_url(self):
        return self.REDIS_URL

settings = Settings()