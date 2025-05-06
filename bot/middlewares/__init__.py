"""
This module initializes and exports the middlewares used in the application.
Exports:
    __middlewares__ (list): A list of middleware instances to be used in the application.
        - ThrottleMiddleware: Middleware that enforces a throttle time to limit the rate of requests.
Attributes:
    __all__ (list): Specifies the public symbols that this module exports.
"""
from bot.middlewares.throttle import ThrottleMiddleware


__all__ = ["__middlewares__"]

__middlewares__ = [
    ThrottleMiddleware(throttle_time=384),
]
