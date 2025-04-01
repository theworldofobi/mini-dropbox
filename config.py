import os
from typing import Dict

# TODO: Implement advanced file-based configuration loading
# TODO: Handle environment-specific overrides

_DEFAULT_CONFIG = {
    "DB_URI": "sqlite:///:memory:",
    "STORAGE_PATH": "/var/data"
}


def load_config() -> Dict[str, str]:
    """
    Gathers environment variables and merges them with default values.

    Returns:
        Dict[str, str]: A dictionary containing the loaded configuration.
    """
    config = {}
    for key, default_value in _DEFAULT_CONFIG.items():
        config[key] = os.environ.get(key, default_value)
    return config


def get_db_uri(config: Dict[str, str]) -> str:
    """
    Returns the database connection string from the provided configuration.

    Args:
        config (Dict[str, str]): A dictionary containing the loaded configuration.

    Returns:
        str: The database connection string.

    Raises:
        ValueError: If 'DB_URI' is not found in the configuration.
    """
    if "DB_URI" not in config:
        raise ValueError("DB_URI not found in configuration.")
    return config["DB_URI"]