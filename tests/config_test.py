import os
import pytest
from unittest.mock import patch, mock_open
import yaml

from config import load_config, get_db_uri, _DEFAULT_CONFIG


@pytest.fixture
def clear_env():
    """
    Fixture to clear environment variables that might affect tests.
    """
    # Save original environment
    original_env = dict(os.environ)
    
    # Clear relevant environment variables
    for key in list(os.environ.keys()):
        if key.startswith("DROPBOX_LITE_"):
            del os.environ[key]
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_load_config_defaults(clear_env):
    """
    Test that load_config() returns defaults when no environment variables are set.
    """
    config_data = load_config()
    assert config_data is not None, "Expected config_data not to be None"
    
    # Check that all default keys are present
    for key in _DEFAULT_CONFIG:
        assert key in config_data, f"{key} should be in the config defaults"
        assert config_data[key] == _DEFAULT_CONFIG[key], f"{key} should have default value"


def test_load_config_from_env(clear_env):
    """
    Test that load_config() correctly reads configuration from environment variables.
    """
    # Set some environment variables
    os.environ["DROPBOX_LITE_HOST"] = "testhost"
    os.environ["DROPBOX_LITE_PORT"] = "9000"
    os.environ["DROPBOX_LITE_DEBUG"] = "false"
    
    config_data = load_config()
    
    # Check that environment variables override defaults
    assert config_data["HOST"] == "testhost"
    assert config_data["PORT"] == 9000  # Should be converted to int
    assert config_data["DEBUG"] is False  # Should be converted to bool


def test_load_config_from_file():
    """
    Test that load_config() correctly reads configuration from a file.
    """
    # Mock file content
    mock_file_content = """
    HOST: filehost
    PORT: 8888
    DEBUG: false
    """
    
    # Mock open to return our file content
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            config_data = load_config("mock_config.yaml")
    
    # Check that file values override defaults
    assert config_data["HOST"] == "filehost"
    assert config_data["PORT"] == 8888
    assert config_data["DEBUG"] is False


def test_get_db_uri():
    """
    Test that get_db_uri() returns the correct database URI.
    """
    config = {"DB_URI": "sqlite:///test.db"}
    assert get_db_uri(config) == "sqlite:///test.db"


def test_get_db_uri_missing():
    """
    Test that get_db_uri() raises an error when DB_URI is missing.
    """
    config = {}
    with pytest.raises(ValueError):
        get_db_uri(config)