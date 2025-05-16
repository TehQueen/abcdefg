import time
import logging

from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottleMiddleware(BaseMiddleware):
    """
    ThrottleMiddleware is a middleware class designed to limit the frequency of user interactions
    with a bot by enforcing a throttle time between consecutive messages from the same user.
    Attributes:
        throttle_time (int): The minimum time interval (in milliseconds) required between
            consecutive messages from the same user. Defaults to 850 ms.
        logger (logging.Logger): Logger instance for logging throttling events.
        user_last_time (dict[int, int]): A dictionary that maps user IDs to the timestamp
            (in milliseconds) of their last interaction.
    Methods:
        __call__(handler, event, data):
            Asynchronously processes incoming messages and enforces throttling. If the time
            elapsed since the user's last message is less than the throttle time, the message
            is ignored, and a log entry is created. Otherwise, the message is passed to the
            handler for further processing.
    """
    def __init__(self, throttle_time: int = 850) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.throttle_time = throttle_time

        # Configuring caching and auto-cleaning settings
        self.user_last_time = TTLCache(maxsize=10_000, ttl=86400)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # pass requests without a user
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = int(time.monotonic() * 1000)
        last_time = self.user_last_time.get(user_id, 0)
        elapsed_time = current_time - last_time

        # Check if the request is too frequent
        if elapsed_time < self.throttle_time:
            self.logger.debug(
                f"Throttled user {user_id}. "
                f"Elapsed: {elapsed_time}ms < {self.throttle_time}ms"
            )
            # Interrupt processing.
            return

        # Update the time and skip the request
        self.user_last_time[user_id] = current_time
        return await handler(event, data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(throttle_time={self.throttle_time})"
