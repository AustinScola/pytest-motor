"""A test file with a multiple tests for TCP/IP socket."""
import asyncio
import socket
from pathlib import Path

import pytest
from pytest_motor.plugin import new_port
# pylint: disable=redefined-outer-name


def test_port_in_range(new_port: int) -> None:
    """Test that port is user available"""
    assert 1024 <= new_port <= 65535


second_port = new_port


def test_ports_not_equals(new_port: int, second_port: int) -> None:
    """Test that fixture doesn't return same ports"""
    assert new_port != second_port


@pytest.mark.asyncio
async def test_port_not_allocated(mongod_binary: Path, new_port: int) -> None:
    """Tests that mongod leaves port free"""
    mongod = await asyncio.create_subprocess_exec(*[str(mongod_binary), '--port', str(new_port)])
    mongod.terminate()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as opened_socket:
        assert opened_socket.connect_ex(('127.0.0.1', new_port)) != 0
