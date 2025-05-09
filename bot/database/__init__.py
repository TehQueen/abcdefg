from typing import Awaitable, Callable, Concatenate
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from bot.database.models import BaseModel


class DatabaseHandler:
    """
    A class to manage database operations, including setting up the engine
    and creating all tables.

    Attributes:
        _engine (AsyncEngine): The asynchronous database engine.
    """
    def __init__(self, dsn: str) -> None:
        """
        Initialize the DatabaseHandler with a given Data Source Name (DSN).

        Args:
            dsn (str): The database connection string.
        """
        self._engine: AsyncEngine = create_async_engine(dsn)

    def __call__[T, R, **P](self, handler: Callable[Concatenate[T, P], Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """
        A decorator to wrap a handler function with a database session.

        Args:
            handler (Callable): The handler function to be wrapped.

        Returns:
            Callable: A wrapped function that provides a database session.
        """
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with AsyncSession(self._engine) as session:
                return await handler(session, *args, **kwargs)
        return wrapper

    async def init(self) -> bool:
        """
        Set up the database engine and create all tables.

        This method initializes the database by creating all defined tables
        using the metadata from the models.
        """
        try:
            async with self._engine.begin() as connection:
                await connection.run_sync(BaseModel.metadata.create_all)
            return True
        except Exception:
            return False


__all__ = ["DatabaseHandler"]
