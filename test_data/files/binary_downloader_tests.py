"""A test file with a multiple tests for mongodb binary downloader."""
from pathlib import Path


def test_binary_downloads(mongod_binary: Path) -> None:
    """Tests if mongod_binary exists"""
    assert mongod_binary.exists()
