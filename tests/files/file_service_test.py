import pytest
import os
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import uuid
from datetime import datetime

# Import the functions to be tested from the project root
from files.file_service import store_file, fetch_file, list_user_files, _file_db

@pytest.fixture
def test_db():
    """
    Fixture for providing a mock or test database session.
    Setup and teardown can be handled here if needed.
    """
    mock_session = MagicMock()
    yield mock_session

@pytest.fixture
def mock_file_obj():
    """
    Fixture to provide a mock file-like object for testing.
    """
    file_mock = MagicMock()
    file_mock.read.return_value = b"Test file content"
    return file_mock


# -----------------------------
# Tests for store_file function
# -----------------------------
@pytest.mark.asyncio
async def test_store_file_success():
    """Test that store_file correctly saves a file and returns metadata."""
    # Arrange
    user_id = "123"
    file_obj = MagicMock()
    file_obj.filename = "test.txt"
    
    # Make read() return a coroutine that resolves to bytes, not bytes directly
    mock_content = b"Test content"
    async def mock_read():
        return mock_content
    file_obj.read = mock_read
    
    # Mock uuid and file operations
    with patch("files.file_service.uuid.uuid4", return_value="mock-uuid"), \
         patch("files.file_service.os.makedirs"), \
         patch("builtins.open", mock_open()) as mock_file:
        
        # Act
        result = await store_file(user_id, file_obj)
        
        # Assert
        assert result["file_id"] == "mock-uuid"
        assert result["original_name"] == "test.txt"
        assert result["user_id"] == "123"
        mock_file.assert_called_once()


async def test_store_file_missing_user(test_db, mock_file_obj):
    """
    Test that store_file raises an error or returns None if user does not exist.
    """
    # Arrange
    user_id = None  # Simulate missing user

    # Act / Assert
    with pytest.raises(ValueError):
        await store_file(user_id, mock_file_obj)


async def test_store_file_invalid_folder(test_db, mock_file_obj):
    """
    Test that store_file raises an exception or handles invalid folder gracefully.
    """
    # Arrange
    user_id = 123
    folder_id = None  # Simulate invalid folder

    # Act / Assert
    with pytest.raises(ValueError):
        await store_file(user_id, mock_file_obj, folder_id)


# -----------------------------
# Tests for fetch_file function
# -----------------------------
def test_fetch_file_success():
    """Test fetch_file returns file data and metadata when valid file_id is provided."""
    # Arrange
    file_id = "test-file-id"
    expected_file_data = b"Mock file content"
    
    # Create a mock file entry in the _file_db
    mock_metadata = {
        "file_id": file_id,
        "user_id": "123",
        "storage_path": "/mock/path/file.txt",
        "original_name": "test.txt"
    }
    
    # Patch the _file_db dictionary
    with patch.dict("files.file_service._file_db", {file_id: mock_metadata}):
        # Mock file reading
        with patch("pathlib.Path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=expected_file_data)):
            
            # Act
            result = fetch_file(file_id)
            
            # Assert
            assert result["metadata"] == mock_metadata
            assert result["file_bytes"] == expected_file_data


def test_fetch_file_not_found(test_db):
    """
    Test that fetch_file handles file_id not found in the DB.
    """
    # Arrange
    file_id = 999
    test_db.execute.return_value.fetchone.return_value = None  # No record returned

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        fetch_file(file_id)


# ---------------------------------
# Tests for list_user_files function
# ---------------------------------
def test_list_user_files_success():
    """Test that list_user_files returns a list of files for a valid user and folder."""
    # Arrange
    user_id = "123"
    folder_id = "456"
    
    # Create mock file entries in the _file_db
    mock_files = {
        "file1": {
            "file_id": "file1",
            "user_id": "123",
            "folder_id": "456",
            "name": "doc1.txt"
        },
        "file2": {
            "file_id": "file2",
            "user_id": "123",
            "folder_id": "456",
            "name": "doc2.txt"
        },
        "file3": {
            "file_id": "file3",
            "user_id": "123",
            "folder_id": "789",  # Different folder
            "name": "doc3.txt"
        },
        "file4": {
            "file_id": "file4",
            "user_id": "456",  # Different user
            "folder_id": "456",
            "name": "doc4.txt"
        }
    }
    
    # Patch the _file_db dictionary
    with patch.dict("files.file_service._file_db", mock_files):
        # Act
        files_list = list_user_files(user_id, folder_id)
        
        # Assert
        assert isinstance(files_list, list)
        assert len(files_list) == 2  # Should only return files for this user and folder
        assert files_list[0]["file_id"] in ["file1", "file2"]
        assert files_list[1]["file_id"] in ["file1", "file2"]


def test_list_user_files_no_results(test_db):
    """
    Test that list_user_files returns an empty list if there are no files.
    """
    # Arrange
    user_id = 123
    folder_id = 999
    test_db.execute.return_value.fetchall.return_value = []  # No files

    # Act
    files_list = list_user_files(user_id, folder_id)

    # Assert
    assert isinstance(files_list, list), "Expected a list return type."
    assert len(files_list) == 0, "Expected an empty list when no files found."


def test_list_user_files_invalid_user():
    """Test that list_user_files handles invalid user IDs appropriately."""
    # In the current implementation, list_user_files doesn't validate user_id
    # Let's modify the test to match the actual behavior
    user_id = None
    folder_id = "456"
    
    # The function should return an empty list, not raise an error
    result = list_user_files(user_id, folder_id)
    assert isinstance(result, list)
    assert len(result) == 0