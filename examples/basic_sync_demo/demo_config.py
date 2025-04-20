import os
from typing import Dict

def load_demo_config() -> Dict[str, str]:
    """
    Loads environment variables or sets defaults for the demo.

    Returns a dict with keys:
      STORAGE_PATH, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS, HOST, PORT, DEBUG, LOG_LEVEL
    """
    config: Dict[str, str] = {}

    try:
        # Where uploaded files are stored
        config["STORAGE_PATH"] = os.environ.get("DEMO_STORAGE_PATH", "uploads")
        config["MAX_CONTENT_LENGTH"] = os.environ.get("MAX_CONTENT_LENGTH", "16777216")  # 16MB
        config["ALLOWED_EXTENSIONS"] = os.environ.get("ALLOWED_EXTENSIONS", "txt,pdf,png,jpg,jpeg,gif")

        # Server configuration
        # Default to 0.0.0.0 so Render can access it externally
        config["HOST"] = os.environ.get("DEMO_HOST", "0.0.0.0")
        # Default to 8000 if DEMO_PORT not set (Render sets PORT automatically)
        config["PORT"] = os.environ.get("DEMO_PORT", "8000")
        config["DEBUG"] = os.environ.get("DEMO_DEBUG", "True")

        # Logging
        config["LOG_LEVEL"] = os.environ.get("DEMO_LOG_LEVEL", "INFO")

    except Exception as exc:
        raise RuntimeError("Failed to load demo configuration.") from exc

    return config
