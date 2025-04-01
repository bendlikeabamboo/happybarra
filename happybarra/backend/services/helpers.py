import logging
from functools import wraps

_logger = logging.getLogger("happybarra")


def logged(logger: logging.Logger = None):
    logger = logger or _logger

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(
                "Executing %s with the following arguments: "
                "{'args'='%s', 'kwargs'='%s'}",
                func.__name__,
                args,
                kwargs,
            )
            result = func(*args, **kwargs)
            logger.debug("%s execution done", func.__name__)
            return result

        return wrapper

    return decorator


def async_logged(logger: logging.Logger = None):
    logger = logger or _logger

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug(
                "Executing %s with the following arguments: "
                "{'args'='%s', 'kwargs'='%s'}",
                func.__name__,
                args,
                kwargs,
            )
            result = func(*args, **kwargs)
            logger.debug("%s execution done", func.__name__)
            return result

        return wrapper

    return decorator
