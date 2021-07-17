"""Test pytest_motor.plugin."""
from asyncio import AbstractEventLoop
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pytest import MonkeyPatch, Testdir, raises

from pytest_motor.plugin import _event_loop, _mongo_ver

# pylint: disable=redefined-outer-name

test_files_directory = Path(__file__).parent.parent / 'test_data' / 'files'
# yapf: disable
test_files = {
    path_to_file.name: path_to_file
    for path_to_file in test_files_directory.glob('*.py')
    if path_to_file.name != '__init__.py'
}
# yapf: enable


@pytest.fixture
def read_conftest() -> str:
    """Reads conftest.py"""
    conftest_file = Path(__file__).parent / 'conftest.py'
    return conftest_file.read_text()


def test_event_loop() -> None:
    """Test pytest_motor.plugin._event_loop."""
    mock_close = Mock(AbstractEventLoop.close)
    mock_event_loop = Mock(AbstractEventLoop, close=mock_close)
    with patch('asyncio.get_event_loop', return_value=mock_event_loop):
        loop_iterator = _event_loop()

        loop = next(loop_iterator)

    assert loop is mock_event_loop

    with pytest.raises(StopIteration):
        next(loop_iterator)

    mock_close.assert_called_once()


def test_new_port(testdir: Testdir, read_conftest: str) -> None:
    """Test pytest_motor.plugin.new_port."""
    assert 'port_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['port_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=3)


def test_mongod_binary_downloader(testdir: Testdir, read_conftest: str) -> None:
    """Test pytest_motor.plugin.mongod_binary."""
    assert 'binary_downloader_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['binary_downloader_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=1)


def test_integration_motor_client(testdir: Testdir, read_conftest: str) -> None:
    """Test pytest_motor.plugin.motor_client."""
    assert 'server_info_test.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['server_info_test.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=1)


def test_integration_clients_independence(testdir: Testdir, read_conftest: str) -> None:
    """Test pytest_motor.plugin.motor_client."""
    assert 'independence_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['independence_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=2)


def test_mongo_ver(monkeypatch: MonkeyPatch) -> None:
    """Test mongo version based on platform system."""
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    assert _mongo_ver() == ("osx", "mongodb-macos-x86_64-4.4.6")

    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert _mongo_ver() == ("linux", "mongodb-linux-x86_64-ubuntu1804-4.4.6")

    monkeypatch.setattr("platform.system", lambda: "Windows")
    with raises(Exception):
        _mongo_ver()
