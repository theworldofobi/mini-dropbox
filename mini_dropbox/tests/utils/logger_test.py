import pytest
from unittest.mock import patch
from typing import NoReturn
from utils.logger import log_debug, log_info, log_error

def test_log_debug_success() -> NoReturn:
    # Test that log_debug logs a standard debug message
    with patch("utils.logger.logger") as mock_logger:
        log_debug("test debug message")
        mock_logger.debug.assert_called_once_with("test debug message")

def test_log_debug_empty_string() -> NoReturn:
    # Test that log_debug handles an empty string correctly
    with patch("utils.logger.logger") as mock_logger:
        log_debug("")
        mock_logger.debug.assert_called_once_with("")

def test_log_debug_none() -> NoReturn:
    # Test that log_debug can handle a None message (though not typical usage)
    with patch("utils.logger.logger") as mock_logger:
        log_debug(None)  # type: ignore
        mock_logger.debug.assert_called_once_with(None)

def test_log_debug_exception(capsys) -> NoReturn:
    # Test that log_debug catches an exception and prints the error
    with patch("utils.logger.logger.debug", side_effect=Exception("Logger not available")):
        log_debug("message causing exception")
        captured = capsys.readouterr()
        assert "Failed to log debug message: Logger not available" in captured.out

def test_log_info_success() -> NoReturn:
    # Test that log_info logs a standard info message
    with patch("utils.logger.logger") as mock_logger:
        log_info("test info message")
        mock_logger.info.assert_called_once_with("test info message")

def test_log_info_empty_string() -> NoReturn:
    # Test that log_info handles an empty string correctly
    with patch("utils.logger.logger") as mock_logger:
        log_info("")
        mock_logger.info.assert_called_once_with("")

def test_log_info_none() -> NoReturn:
    # Test that log_info can handle a None message (though not typical usage)
    with patch("utils.logger.logger") as mock_logger:
        log_info(None)  # type: ignore
        mock_logger.info.assert_called_once_with(None)

def test_log_info_exception(capsys) -> NoReturn:
    # Test that log_info catches an exception and prints the error
    with patch("utils.logger.logger.info", side_effect=Exception("Logger not available")):
        log_info("message causing exception")
        captured = capsys.readouterr()
        assert "Failed to log info message: Logger not available" in captured.out

def test_log_error_success() -> NoReturn:
    # Test that log_error logs a standard error message
    with patch("utils.logger.logger") as mock_logger:
        log_error("test error message")
        mock_logger.error.assert_called_once_with("test error message")

def test_log_error_empty_string() -> NoReturn:
    # Test that log_error handles an empty string correctly
    with patch("utils.logger.logger") as mock_logger:
        log_error("")
        mock_logger.error.assert_called_once_with("")

def test_log_error_none() -> NoReturn:
    # Test that log_error can handle a None message (though not typical usage)
    with patch("utils.logger.logger") as mock_logger:
        log_error(None)  # type: ignore
        mock_logger.error.assert_called_once_with(None)

def test_log_error_exception(capsys) -> NoReturn:
    # Test that log_error catches an exception and prints the error
    with patch("utils.logger.logger.error", side_effect=Exception("Logger not available")):
        log_error("message causing exception")
        captured = capsys.readouterr()
        assert "Failed to log error message: Logger not available" in captured.out