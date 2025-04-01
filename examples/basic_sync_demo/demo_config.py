import os
from typing import Dict

def load_demo_config() -> Dict[str, str]:
    """
    Loads environment variables or sets defaults for the demo.

    This function reads relevant environment variables for the demo configuration
    or sets default values if they are not provided.

    Returns:
        Dict[str, str]: A dictionary containing the demo configuration.
    """
    config: Dict[str, str] = {}

    try:
        # Basic placeholder values
        # TODO: Add or remove environment variable lookups as needed
        config["DB_CONNECTION"] = os.environ.get("DEMO_DB_CONNECTION", "sqlite:///:memory:")
        config["STORAGE_PATH"] = os.environ.get("DEMO_STORAGE_PATH", "/tmp/demo_storage")
        config["LOG_LEVEL"] = os.environ.get("DEMO_LOG_LEVEL", "INFO")
    except Exception as exc:
        # Handle unexpected errors during config loading
        raise RuntimeError("Failed to load demo configuration.") from exc

    return config