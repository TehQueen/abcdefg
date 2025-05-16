import time
import logging

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class HighPerformanceThrottleMiddleware(BaseMiddleware):
    """
    HighPerformanceThrottleMiddleware is a middleware class designed to limit the frequency
    of user interactions with a bot by enforcing a throttle time between consecutive updates
    from the same user.

    Methods:
        __call__(handler, event, data):
            Asynchronously processes incoming updates and enforces throttling. If the time
            elapsed since the user's last message is less than the throttle time, the message
            is ignored, and a log entry is created. Otherwise, the message is passed to the
            handler for further processing.
    """
    __slots__ = ('limits', 'buckets', 'logger', 'cache_size')

    def __init__(
        self,
        default_rps: int = 5,
        burst_capacity: int = 10,
        cache_size: int = 25_000
    ) -> None:
        """
        Create an instance of middleware

        :param default_rps: Base rate limit - how many requests per second a user is
            allowed on average. The default value is 5.
        :param burst_capacity: The maximum number of requests a user can make instantly
            before the limit is reached. The default value is 10.
        :param cache_size: The maximum number of unique users for which the throttling
            status is maintained. The default value is 25_000.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.cache_size = cache_size
        
        # Atomic data structure: {user_id: (tokens,last_update)}
        self.buckets = {}
        
        # Configuration of restrictions
        self.limits = {
            "default": (default_rps, burst_capacity),
            "callback": (18, 24),
            "command": (6, 7),
            "message": (3, 5)
        }

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        
        if not user:
            return await handler(event, data)

        user_id = user.id
        event_type = self._detect_event_type(event)
        now = time.monotonic()

        # Atomic operations without locks
        tokens, last = self.buckets.get(user_id, (0, now))
        
        # Calculation of new tokens
        elapsed = now - last
        rate, capacity = self.limits.get(event_type, self.limits["default"])
        new_tokens = min(capacity, tokens + elapsed * rate)
        
        # Check and update in one step
        if new_tokens >= 1:
            self.buckets[user_id] = (new_tokens - 1, now)
            return await handler(event, data)
        else:
            self.buckets[user_id] = (new_tokens, now)
            self._log_throttle(user_id, event_type)
            return

    def _detect_event_type(self, event: TelegramObject) -> str:
        """Quick classification of events"""
        if isinstance(event, Message):
            return "command" if event.text.startswith('/') else "message"
        if isinstance(event, CallbackQuery):
            return "callback"
        return "other"

    def _log_throttle(self, user_id: int, event_type: str) -> None:
        """Optimized logging"""
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Throttled {user_id} ({event_type})")

    def __repr__(self) -> str:
        return f"HighPerfThrottle(default_rps={self.limits['default'][0]})"
