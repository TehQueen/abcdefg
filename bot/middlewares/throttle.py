import time
import logging

from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject


class AdvancedThrottleMiddleware(BaseMiddleware):
    """
    AdvancedThrottleMiddleware is a middleware class designed to limit the frequency of user
    interactions with a bot by enforcing a throttle time between consecutive messages from
    the same user.

    Methods:
        __call__(handler, event, data):
            Asynchronously processes incoming messages and enforces throttling. If the time
            elapsed since the user's last message is less than the throttle time, the message
            is ignored, and a log entry is created. Otherwise, the message is passed to the
            handler for further processing.
    """
    def __init__(
        self,
        default_limit: int = 5,
        per_seconds: int = 10,
        burst_protection: bool = True,
        event_type_limits: Optional[Dict[str, Dict]] = None
    ) -> None:
        """
        Create an instance of middleware

        :param default_limit: The number of updates during the time interval specified in the
            "per_second" attribute. The default value is 5u.
        :param per_seconds: The minimum time interval (in seconds) required between consecutive
            messages from the same user. The default value is 10s.
        :param burst_protection: Enable burst attack checking. The default value is True.
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Setting restrictions
        self.default_limit = default_limit
        self.per_seconds = per_seconds
        self.burst_protection = burst_protection
        self.event_limits = event_type_limits or {}
        
        # Configuring caching and auto-cleaning settings
        self.request_history = TTLCache(maxsize=10_000, ttl=per_seconds * 2)
        
        # Statistics for adaptive throttling
        self.total_requests = 0
        self.blocked_requests = 0

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Pass requests without a user
        if not getattr(event, "from_user", None):
            return await handler(event, data)

        user_id = event.from_user.id
        event_type = self._get_event_type(event)
        current_time = time.monotonic()

        # Get restrictions for event type
        limits = self.event_limits.get(event_type, {
            "limit": self.default_limit,
            "per_seconds": self.per_seconds
        })

        # Initializing the query history
        if user_id not in self.request_history:
            self.request_history[user_id] = {}

        user_history = self.request_history[user_id]
        
        # Statistics update
        self.total_requests += 1

        # Checking restrictions
        if self._check_limits(user_history, event_type, current_time, limits):
            self.blocked_requests += 1
            self.logger.warning(
                f"Throttled user {user_id} ({event_type}). "
                f"Limit: {limits['limit']}/{limits['per_seconds']}s"
            )
            return
        else:
            # Update history on successful request
            self._update_history(user_history, event_type, current_time)
            return await handler(event, data)

    def _get_event_type(self, event: TelegramObject) -> str:
        """Defining the event type for differentiated regulation"""
        if isinstance(event, Message):
            if event.text.startswith('/'):
                return "command"
            return "message"
        if isinstance(event, CallbackQuery):
            return "callback"
        return "other"

    def _check_limits(
        self,
        history: Dict,
        event_type: str,
        current_time: float,
        limits: Dict
    ) -> bool:
        """Constraint checking using sliding window algorithm"""
        # Initializing history for event type
        if event_type not in history:
            history[event_type] = []

        # Clearing old records
        window_start = current_time - limits["per_seconds"]
        history[event_type] = [
            t for t in history[event_type] if t > window_start
        ]

        # Checking burst attacks
        if self.burst_protection and len(history[event_type]) >= limits["limit"]:
            return True

        # Adaptive limiting under high load
        if self._high_load_condition():
            return len(history[event_type]) >= max(1, limits["limit"] // 2)

        return False

    def _update_history(self, history: Dict, event_type: str, timestamp: float):
        """Updating query history"""
        history[event_type].append(timestamp)
        
        # Optimization of stored data
        if len(history[event_type]) > self.default_limit * 2:
            history[event_type] = history[event_type][-self.default_limit:]

    def _high_load_condition(self) -> bool:
        """Adaptive limiting under high load"""
        if self.total_requests == 0:
            return False
        block_ratio = self.blocked_requests / self.total_requests
        # Limits are reduced if we block less than 10%
        return block_ratio < 0.1

    def __repr__(self) -> str:
        return (
            f"AdvancedThrottle("
            f"default={self.default_limit}/{self.per_seconds}s, "
            f"burst_protection={self.burst_protection})"
        )
