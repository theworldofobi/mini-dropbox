import logging
import logging.handlers
import os
from typing import NoReturn
from datetime import datetime
from config import load_config

# Load configuration
config = load_config()

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create formatters
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler for all logs
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOGS_DIR, 'dropbox_lite.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Error file handler
error_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOGS_DIR, 'error.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(file_formatter)
logger.addHandler(error_handler)

def log_debug(message: str) -> None:
    """Logs a debug-level message."""
    try:
        logger.debug(message)
    except Exception as e:
        # Fallback to print if logging fails
        print(f"[DEBUG] {datetime.now()} - {message}")
        print(f"Logging failed: {e}")

def log_info(message: str) -> None:
    """Logs an info-level message."""
    try:
        logger.info(message)
    except Exception as e:
        # Fallback to print if logging fails
        print(f"[INFO] {datetime.now()} - {message}")
        print(f"Logging failed: {e}")

def log_error(message: str) -> None:
    """Logs an error-level message."""
    try:
        logger.error(message, exc_info=True)
    except Exception as e:
        # Fallback to print if logging fails
        print(f"[ERROR] {datetime.now()} - {message}")
        print(f"Logging failed: {e}")

def log_critical(message: str) -> NoReturn:
    """Logs a critical error and raises an exception."""
    try:
        logger.critical(message, exc_info=True)
        raise SystemExit(message)
    except Exception as e:
        # Fallback to print if logging fails
        print(f"[CRITICAL] {datetime.now()} - {message}")
        print(f"Logging failed: {e}")
        raise SystemExit(f"Critical error: {message}")