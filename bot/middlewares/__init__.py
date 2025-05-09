"""
This module initializes and exports middleware components for the bot.
Modules:
    throttle: Contains the `ThrottleMiddleware` class, which is responsible for
              rate-limiting and throttling requests to ensure proper handling of
              incoming traffic.
    authoriz: Contains the `AuthorizationMiddleware` class, which manages user
              authorization and access control for the bot.
Exports:
    ThrottleMiddleware: Middleware for handling request throttling.
"""
from bot.middlewares.throttle import ThrottleMiddleware


__all__ = [
    "ThrottleMiddleware",
]
