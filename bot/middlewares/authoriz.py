from typing import Any, Awaitable, Callable, Dict, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser

from bot.database.handlers.auth import check_if_auth, add_user
from bot.database.models import User

# Type aliases for better readability
HandlerType: TypeAlias = Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]


class AuthorizationMiddleware(BaseMiddleware):
    """
    Middleware for handling user authorization.

    Performs the following functions:
        * Checks if the user is logged in
        * Creates a new user record on first contact
        * Adds the user object to the data context
    """
    def __init__(self) -> None:
        """
        Create an instance of middleware
        """
        super().__init__()

    async def __call__(
        self,
        handler: HandlerType,
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Main middleware processing pipeline."""
        
        # Checking user information
        if not (tuser := getattr(event, "from_user", None)):
            return await handler(event, data)

        # Check if user exists in database
        if not (duser := await check_if_auth(tuser.id)):
            # Create a new user on first interaction
            duser = await self._create_new_user(tuser)

        # Adding a user to the data context
        data['user'] = duser

        # We continue the processing chain
        return await handler(event, data)
    
    @staticmethod
    async def _create_new_user(user_data: TelegramUser) -> User:
        """
        Creates a new user in the database.

        Arguments:
            user_data: User data from Telegram

        Returns:
            User object created
        """
        return await add_user(
            User(
                id=user_data.id,
                username=user_data.username,
                full_name=user_data.full_name,
                language_code=user_data.language_code
            )
        )
