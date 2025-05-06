"""
This module defines the configuration settings for the bot application using Pydantic's BaseSettings.
Classes:
    Settings:
        A Pydantic BaseSettings subclass that holds configuration values for the bot and database.
        It includes a property to generate the database connection string (DSN).
Attributes:
    settings (Settings):
        An instance of the Settings class, which loads the configuration values.
Settings Attributes:
    BOT_TOKEN (str):
        The token used to authenticate the bot with the messaging platform.
    DB_USER (str):
        The username for connecting to the database. Defaults to "postgres".
    DB_PSWD (str):
        The password for connecting to the database. Defaults to "postgres".
    DB_HOST (str):
        The hostname or IP address of the database server. Defaults to "localhost".
    DB_PORT (str):
        The port number on which the database server is listening. Defaults to "5432".
    DB_NAME (str):
        The name of the database to connect to. Defaults to "postgres".
    DB_DRIVER (str):
        The database driver used for the connection. Defaults to "postgresql+asyncpg".
Methods:
    DSN (property):
        Constructs and returns the database connection string (DSN) based on the database configuration attributes.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    # Bot configuration
    BOT_TOKEN: str

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
