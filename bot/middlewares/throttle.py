import logging

from time import time
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
        self.user_last_time = dict[int, int]()
        self.throttle_time = throttle_time

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message, data: Dict[str, Any]) -> Any:
        uid = event.from_user.id
        current_time = int(time() * 1000)

        last_time = self.user_last_time.get(uid, 0)
        elapsed_time = current_time - last_time
        ratio = self.throttle_time / elapsed_time

        if (elapsed_time > self.throttle_time) and (ratio <= 0.4):
            self.user_last_time[uid] = current_time
            return await handler(event, data)
        else:
            self.logger.info(f"User {uid} is throttled. Waiting for {self.throttle_time} ms.")
            self.user_last_time[uid] = current_time

    def __repr__(self):
        return f"ThrottleMiddleware(throttle_time={self.throttle_time})"
