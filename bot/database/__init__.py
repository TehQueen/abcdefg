from __future__ import annotations

from contextlib import asynccontextmanager
from functools import wraps
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Concatenate,
    ParamSpec,
    Self,
    TypeAlias,
    TypeVar,
    overload
)

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from bot.database.models import BaseModel


P = ParamSpec("P")
R = TypeVar("R")
SessionHandler: TypeAlias = Callable[Concatenate[AsyncSession, P], Awaitable[R]]
WrappedHandler: TypeAlias = Callable[P, Awaitable[R]]

class DatabaseHandler:
    """Asynchronous DB handler with session and transaction management"""
    
    def __init__(self, dsn: str, **kwargs: Any) -> None:
        self._engine = create_async_engine(
            dsn,
            future=True,
            pool_pre_ping=True,
            **kwargs
        )

    @overload
    def __call__(self, handler: SessionHandler[P, R]) -> WrappedHandler[P, R]: ...
    
    @overload
    def __call__(self, **session_kwargs: Any) -> Self: ...

    def __call__(
            self,
            handler: SessionHandler[P, R] | None = None,
            **session_kwargs: Any
    ) -> WrappedHandler[P, R]:

        if handler is None:
            # Returning a new instance
            return type(self)(self._engine.url)

        @wraps(handler)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            async with self.session(**session_kwargs) as session:
                return await handler(session, *args, **kwargs)
                
        return wrapped

    @asynccontextmanager
    async def session(self, **kwargs: Any) -> AsyncIterator[AsyncSession]:
        """Asynchronous context manager for session"""
        async with AsyncSession(self._engine, **kwargs) as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def init(self) -> bool:
        """Initializing the DB schema"""
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        return True

    async def close(self) -> None:
        """Correctly closing connections"""
        await self._engine.dispose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

__all__ = ["DatabaseHandler"]
