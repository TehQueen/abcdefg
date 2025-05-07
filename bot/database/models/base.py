from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(AsyncAttrs, DeclarativeBase): ...
"""
BaseModel serves as the foundational class for all database models in the application.

It inherits from `AsyncAttrs` and `DeclarativeBase`, providing asynchronous attribute
support and declarative base functionality for SQLAlchemy ORM models.

Attributes and methods defined in this class are shared across all derived models,
ensuring consistency and reusability in the database layer.
"""
