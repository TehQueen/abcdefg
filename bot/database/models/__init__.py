"""
This module initializes the database models for the application.
It imports and exposes the following models:
- `BaseModel`: The base class for all database models, providing common functionality.
- `User`: The model representing user-related data.
The `__all__` variable is defined to explicitly specify the public API of this module.
"""
from bot.database.models.base import BaseModel
from bot.database.models.user import User

__all__ = ["BaseModel", "User"]
