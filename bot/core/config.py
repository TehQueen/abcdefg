import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Bot configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # Database configuration
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PSWD: str = os.getenv("DB_PSWD", "postgres")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "postgres")

    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql+asyncpg")

    DSN: str = f"{DB_DRIVER}://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()
