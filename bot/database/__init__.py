from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from bot.database import handlers, models


class DatabaseHandler:
    """
    A class to manage database operations, including setting up the engine
    and creating all tables.

    Attributes:
        __models__ (list): List of all models defined in the `models` module.
        __handlers__ (list): List of all handlers defined in the `handlers` module.
        _engine (AsyncEngine): The asynchronous database engine.
    """
    __models__: list[str] = models.__all__
    __handlers__: list[str] = handlers.__all__

    def __init__(self, dsn: str) -> None:
        """
        Initialize the DatabaseHandler with a given Data Source Name (DSN).

        Args:
            dsn (str): The database connection string.
        """
        self._engine: AsyncEngine = create_async_engine(dsn)

    async def __call__(self) -> None:
        """
        Set up the database engine and create all tables.

        This method initializes the database by creating all defined tables
        using the metadata from the models.
        """
        async with self._engine.begin() as connection:
            await connection.run_sync(models.BaseModel.metadata.create_all)


__all__ = ["DatabaseHandler"]
