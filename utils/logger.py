import logging
from typing import NoReturn

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# TODO: Configure logging handlers and formatters as required

def log_debug(message: str) -> None:
    """
    Logs a debug-level message.

    Args:
        message: The message to log.
    """
    try:
        logger.debug(message)
    except Exception as e:
        # TODO: Implement alternative logging mechanism if needed
        print(f"Failed to log debug message: {e}")

def log_info(message: str) -> None:
    """
    Logs an info-level message.

    Args:
        message: The message to log.
    """
    try:
        logger.info(message)
    except Exception as e:
        # TODO: Implement alternative logging mechanism if needed
        print(f"Failed to log info message: {e}")

def log_error(message: str) -> None:
    """
    Logs an error-level message.

    Args:
        message: The message to log.
    """
    try:
        logger.error(message)
    except Exception as e:
        # TODO: Implement alternative logging mechanism if needed
        print(f"Failed to log error message: {e}")