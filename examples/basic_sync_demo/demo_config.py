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
        # Configuration for the demo web interface
        config["UPLOAD_FOLDER"] = os.environ.get("DEMO_STORAGE_PATH", "uploads")
        config["MAX_CONTENT_LENGTH"] = os.environ.get("MAX_CONTENT_LENGTH", "16777216")  # 16MB
        config["ALLOWED_EXTENSIONS"] = os.environ.get("ALLOWED_EXTENSIONS", "txt,pdf,png,jpg,jpeg,gif")
        
        # Server configuration
        config["HOST"] = os.environ.get("DEMO_HOST", "localhost")
        config["PORT"] = os.environ.get("DEMO_PORT", "5000")
        config["DEBUG"] = os.environ.get("DEMO_DEBUG", "True")
        
        # Logging configuration
        config["LOG_LEVEL"] = os.environ.get("DEMO_LOG_LEVEL", "INFO")
        
    except Exception as exc:
        # Handle unexpected errors during config loading
        raise RuntimeError("Failed to load demo configuration.") from exc

    return config