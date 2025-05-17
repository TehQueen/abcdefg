from __future__ import annotations

import time
import math
import logging

from collections import deque
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

# Type aliases for better readability
Bucket: TypeAlias = Tuple[float, float]
HandlerType: TypeAlias = Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]


class AutoTunedThrottlingMiddleware(BaseMiddleware):
    """
    Advanced auto-tuning throttling middleware implementing:
    - Token bucket algorithm with dynamic parameters
    - PID-controlled rate adjustment
    - System pressure awareness
    - Burst capacity optimization
    
    Features:
    - Zero-dependency implementation
    - Lock-free atomic operations
    - Memory-efficient storage
    - Real-time metrics collection
    - Self-optimizing parameters
    """

    __slots__ = (
        "_buckets",
        "_logger",
        "_cache_size",
        "_metrics",
        "_adaptive_cooldown",
        "_current_rps",
        "_max_rps",
        "_min_rps",
        "_burst_factor",
        "_pressure_window",
    )

    def __init__(
        self,
        initial_rps: float = 10.0,
        max_rps: float = 80.0,
        min_rps: float = 4.0,
        cache_size: int = 25_000,
        pressure_window: int = 60,
    ) -> None:
        """
        Create an instance of middleware

        :param initial_rps: Initial requests per second limit
        :param max_rps: Maximum allowable requests per second
        :param min_rps: Minimum allowable requests per second
        :param cache_size: Maximum number of users to track
        :param pressure_window: Metrics collection window in seconds
        """
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cache_size = cache_size
        self._pressure_window = pressure_window

        # Rate limiting parameters
        self._current_rps = initial_rps
        self._max_rps = max_rps
        self._min_rps = min_rps

        # Initial burst multiplier
        self._burst_factor = 2.0

        # State storage
        self._buckets: Dict[int, Bucket] = {}
        
        # Metrics collection
        self._metrics = {
            "total_requests": 0,
            "blocked_requests": 0,
            "latencies": deque[float](maxlen=1000),
            "pressure": 0.0,
        }
        
        # Adaptive tuning state
        self._adaptive_cooldown = time.monotonic()

    async def __call__(
        self,
        handler: HandlerType,
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        """Main middleware processing pipeline."""
        start_time = time.monotonic()
        
        try:
            if not (user := getattr(event, "from_user", None)):
                return await handler(event, data)

            user_id = user.id
            event_type = self._classify_event(event)

            # Get or create bucket with atomic operations
            tokens, last_update = self._buckets.get(
                user_id,
                (self.burst_capacity, start_time)
            )
            
            # Calculate token replenishment
            elapsed = start_time - last_update
            new_tokens = min(
                self.burst_capacity,
                tokens + elapsed * self._current_rps,
            )

            # Process request if tokens available
            if new_tokens >= 1.0:
                self._buckets[user_id] = (new_tokens - 1.0, start_time)
                result = await handler(event, data)
                self._update_metrics(start_time, blocked=False)
                return result

            # Block request and update metrics
            self._buckets[user_id] = (new_tokens, start_time)
            self._update_metrics(start_time, blocked=True)
            self._log_throttle_event(user_id, event_type)
            return None

        finally:
            self._auto_tune()

    @property
    def burst_capacity(self) -> float:
        """Dynamic burst capacity calculated from current RPS and burst factor."""
        return self._current_rps * self._burst_factor

    def _classify_event(self, event: TelegramObject) -> str:
        """Classify events for future differential throttling support."""
        if isinstance(event, CallbackQuery):
            return "callback"
        if isinstance(event, Message):
            return "command" if (t := event.text) and t.startswith('/') else "command"
        return isinstance(event, CallbackQuery) and "callback" or "other"

    def _update_metrics(self, start_time: float, blocked: bool) -> None:
        """Update performance metrics and system pressure calculations."""
        latency = time.monotonic() - start_time
        self._metrics["latencies"].append(latency)
        self._metrics["total_requests"] += 1
        self._metrics["blocked_requests"] += int(blocked)
        self._metrics["pressure"] = self._calculate_pressure()

    def _calculate_pressure(self) -> float:
        """Calculate system pressure based on latency percentiles."""
        if not self._metrics["latencies"]:
            return 0.0

        sorted_latencies = sorted(self._metrics["latencies"])
        count = len(sorted_latencies)
        
        avg = sum(sorted_latencies) / count
        p95 = sorted_latencies[int(count * 0.95)]

        # Normalized pressure indicator
        return min(1.0, avg / p95)

    def _auto_tune(self) -> None:
        """Adaptive parameter tuning using control theory principles."""
        if (now := time.monotonic()) - self._adaptive_cooldown < 5.0:
            return

        # Calculate control parameters
        pressure = self._metrics["pressure"]
        total = self._metrics["total_requests"]
        blocked = self._metrics["blocked_requests"]
        block_rate = blocked / total if total > 0 else 0.0

        # PID-like controller for RPS adjustment
        p_error = 0.7 - pressure  # Target pressure = 0.7
        i_error = 0.1 - block_rate  # Target block rate = 10%
        adjustment = (0.5 * p_error) + (0.01 * i_error) - (0.1 * pressure)
        rps_change = math.tanh(adjustment) * 0.1  # ±10% max change

        # Burst factor adaptation
        burst_change = (
            -0.05 if block_rate > 0.2 else
            0.02 if block_rate < 0.05 else
            0.0
        )

        # Apply changes with clamping
        self._current_rps = sorted((
            self._current_rps * (1 + rps_change),
            self._min_rps,
            self._max_rps,
        ))[1]

        self._burst_factor = sorted((
            self._burst_factor * (1 + burst_change),
            1.5,
            3.0,
        ))[1]

        # Reset metrics and update cooldown
        self._metrics.update({"total_requests": 0, "blocked_requests": 0})
        self._adaptive_cooldown = now

    def _log_throttle_event(self, user_id: int, event_type: str) -> None:
        """Optimized logging with level checking before formatting."""
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(
                f"Throttled event: user={user_id}, "
                f"type={event_type}, "
                f"current_rps={self._current_rps:.1f}, "
                f"burst={self.burst_capacity:.1f}"
            )

    def cleanup_old_buckets(self) -> None:
        """LRU-based cache eviction for memory management."""
        if len(self._buckets) <= self._cache_size:
            return

        # Sort buckets by last access time
        lru = sorted(
            self._buckets.items(),
            key=lambda item: item[1][1],
            reverse=True,
        )

        # Keep only most recent entries
        self._buckets = dict(lru[:self._cache_size])

    @property
    def current_parameters(self) -> Dict[str, float]:
        """Current rate limiting parameters for monitoring."""
        return {
            "rps": self._current_rps,
            "burst_capacity": self.burst_capacity,
            "burst_factor": self._burst_factor,
            "pressure": self._metrics["pressure"],
            "cache_usage": len(self._buckets) / self._cache_size,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"current_rps={self._current_rps:.1f}, "
            f"burst={self.burst_capacity:.1f}, "
            f"pressure={self._metrics['pressure']:.2f})"
        )
