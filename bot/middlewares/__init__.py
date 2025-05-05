from .throttle import ThrottleMiddleware


__middlewares__ = [
    ThrottleMiddleware(throttle_time=384),
]

__all__ = []
