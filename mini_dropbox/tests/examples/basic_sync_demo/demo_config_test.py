from typing import Dict
import pytest
from unittest.mock import patch
import os
from examples.basic_sync_demo.demo_config import load_demo_config

@pytest.fixture
def clear_env():
    original_env = dict(os.environ)
    for var in ["DEMO_DB_CONNECTION", "DEMO_STORAGE_PATH", "DEMO_LOG_LEVEL"]:
        os.environ.pop(var, None)
    yield
    os.environ.clear()
    os.environ.update(original_env)

def test_load_demo_config_defaults(clear_env):
    # Ensures that when no env variables are set, defaults are returned
    config = load_demo_config()
    assert config["DB_CONNECTION"] == "sqlite:///:memory:"
    assert config["STORAGE_PATH"] == "/tmp/demo_storage"
    assert config["LOG_LEVEL"] == "INFO"

def test_load_demo_config_custom(clear_env):
    # Ensures that when env variables are set, the corresponding values are used
    os.environ["DEMO_DB_CONNECTION"] = "sqlite:///custom.db"
    os.environ["DEMO_STORAGE_PATH"] = "/custom/storage/path"
    os.environ["DEMO_LOG_LEVEL"] = "DEBUG"
    config = load_demo_config()
    assert config["DB_CONNECTION"] == "sqlite:///custom.db"
    assert config["STORAGE_PATH"] == "/custom/storage/path"
    assert config["LOG_LEVEL"] == "DEBUG"

def test_load_demo_config_error():
    # Ensures that an unexpected exception is re-raised as RuntimeError
    with patch("os.environ.get", side_effect=Exception("Unexpected")):
        with pytest.raises(RuntimeError) as exc_info:
            load_demo_config()
        assert "Failed to load demo configuration." in str(exc_info.value)