#-----------------------
# Cache
#-----------------------
"""Caching decorator for Smart Farm project."""

import functools
import time
from agents.tools.utils.logger import log

_cache = {}

def cache_result(ttl=300):
    """Cache function results for a specified TTL (seconds)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in _cache:
                result, timestamp = _cache[key]
                if now - timestamp < ttl:
                    log(f"Cache hit for {func.__name__}")
                    return result
            result = func(*args, **kwargs)
            _cache[key] = (result, now)
            log(f"Cache stored for {func.__name__}")
            return result
        return wrapper
    return decorator
