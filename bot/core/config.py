"""
This module defines the `Settings` class for managing application configuration
using Pydantic's `BaseSettings`. It provides a structured way to handle environment
variables and default values for various settings.
Classes:
    - Settings: A Pydantic-based configuration class that includes settings for
      bot configuration, localization, scheduler, and database connection.
Attributes:
    - BOT_TOKEN (str): The bot token for authentication.
    - LOG_DIR (str): Path to the directory containing log files.
    - LOG_FILE (str): Current log file name.
    - LOCALE_DIR (str): Path to the directory containing localization files.
    - LOCALE_DOMAIN (str): Domain name for localization messages.
    - LOCALE_FALLBACK (str): Fallback language for localization.
    - SCHEDULER_TIMEZONE (str): Timezone for the scheduler.
    - DB_USER (str): Database username.
    - DB_PSWD (str): Database password.
    - DB_HOST (str): Database host address.
    - DB_PORT (str): Database port number.
    - DB_NAME (str): Database name.
    - DB_DRIVER (str): Database driver for connection.
Properties:
    - DSN (str): Constructs and returns the database connection string (DSN)
      based on the database configuration attributes.
"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configuration model settings
    model_config = SettingsConfigDict(validate_default=False)

    # Bot configuration
    BOT_TOKEN: str

    # Logging configuration
    LOG_DIR: str = "/var/log/tb"
    LOG_FILE: str = str(Path(LOG_DIR) / "app.log")

    # Localization configuration
    LOCALE_DIR: str = str(Path(__file__).parent.parent / "locales")
    LOCALE_DOMAIN: str = "messages"
    LOCALE_FALLBACK: str = "en"

    # Scheduler configuration
    SCHEDULER_TIMEZONE: str = "Europe/Moscow"

    # Database configuration
    DB_USER: str = "postgres"
    DB_PSWD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"

    @property
    def DSN(self) -> str:
        return (
            f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PSWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
