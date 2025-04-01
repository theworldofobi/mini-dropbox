from typing import Dict
import pytest
import os
from config import load_config, get_db_uri

def test_load_config_default(monkeypatch: pytest.MonkeyPatch) -> None:
    # Ensure no environment variables are set
    for var in ["DB_URI", "STORAGE_PATH"]:
        monkeypatch.delenv(var, raising=False)
    config = load_config()
    assert config["DB_URI"] == "sqlite:///:memory:"
    assert config["STORAGE_PATH"] == "/var/data"

def test_load_config_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    # Override environment variables
    monkeypatch.setenv("DB_URI", "postgresql://user:pass@localhost:5432/mydb")
    monkeypatch.setenv("STORAGE_PATH", "/custom/path")
    config = load_config()
    assert config["DB_URI"] == "postgresql://user:pass@localhost:5432/mydb"
    assert config["STORAGE_PATH"] == "/custom/path"

def test_get_db_uri_success() -> None:
    # Provide a valid config that includes DB_URI
    config = {"DB_URI": "postgresql://user:pass@localhost/mydb"}
    db_uri = get_db_uri(config)
    assert db_uri == "postgresql://user:pass@localhost/mydb"

def test_get_db_uri_missing_key() -> None:
    # Provide a config without DB_URI to ensure ValueError is raised
    config = {}
    with pytest.raises(ValueError, match="DB_URI not found in configuration."):
        get_db_uri(config)