import os
from typing import Dict, Any
import yaml
import logging

logger = logging.getLogger(__name__)

# TODO: Implement advanced file-based configuration loading
# TODO: Handle environment-specific overrides

# Default configuration
_DEFAULT_CONFIG = {
    "DB_URI": "sqlite:///:memory:",
    "STORAGE_PATH": "uploads",
    "MAX_FILE_SIZE": 100 * 1024 * 1024,  # 100MB
    "ALLOWED_EXTENSIONS": [".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif"],
    "JWT_SECRET_KEY": "your-secret-key",  # Change in production
    "JWT_ALGORITHM": "HS256",
    "JWT_EXPIRE_MINUTES": 30,
    "HOST": "localhost",
    "PORT": 8000,
    "DEBUG": True,
    "LOG_LEVEL": "INFO"
}

def load_config(config_file: str = None) -> Dict[str, Any]:
    """Loads configuration from file and environment variables."""
    config = _DEFAULT_CONFIG.copy()
    
    try:
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                config.update(file_config)
        
        # Override with environment variables
        for key in config:
            env_value = os.environ.get(f"DROPBOX_LITE_{key}")
            if env_value is not None:
                # Convert string values to appropriate types
                if isinstance(config[key], bool):
                    config[key] = env_value.lower() == "true"
                elif isinstance(config[key], int):
                    config[key] = int(env_value)
                elif isinstance(config[key], list):
                    config[key] = env_value.split(",")
                else:
                    config[key] = env_value
        
        logger.info("Configuration loaded successfully")
        return config
        
    except Exception as e:
        logger.error("Failed to load configuration: %s", str(e))
        raise RuntimeError(f"Failed to load configuration: {str(e)}") from e

def get_db_uri(config: Dict[str, Any]) -> str:
    """Returns database URI from config."""
    if "DB_URI" not in config:
        raise ValueError("DB_URI not found in configuration")
    return config["DB_URI"]