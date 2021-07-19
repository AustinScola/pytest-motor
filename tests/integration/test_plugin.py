"""Integration tests for the plugin."""
from asyncio import AbstractEventLoop
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pytest import Testdir

test_files_directory = Path(__file__).parent.parent.parent / 'test_data' / 'files'
# yapf: disable
test_files = {
    path_to_file.name: path_to_file
    for path_to_file in test_files_directory.glob('*.py')
    if path_to_file.name != '__init__.py'
}
# yapf: enable

pytestmark = pytest.mark.integration

@pytest.fixture
def read_conftest() -> str:
    """Reads conftest.py"""
    conftest_file = Path(__file__).parent.parent / 'conftest.py'
    return conftest_file.read_text()


def test_new_port(testdir: Testdir, read_conftest: str) -> None:
    # pylint: disable=redefined-outer-name
    """Test pytest_motor.plugin.new_port."""
    assert 'port_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['port_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=3)


def test_mongod_binary_downloader(testdir: Testdir, read_conftest: str) -> None:
    # pylint: disable=redefined-outer-name
    """Test pytest_motor.plugin.mongod_binary."""
    assert 'binary_downloader_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['binary_downloader_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=1)


def test_integration_motor_client(testdir: Testdir, read_conftest: str) -> None:
    # pylint: disable=redefined-outer-name
    """Test pytest_motor.plugin.motor_client."""
    assert 'server_info_test.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['server_info_test.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=1)


def test_integration_clients_independence(testdir: Testdir, read_conftest: str) -> None:
    # pylint: disable=redefined-outer-name
    """Test pytest_motor.plugin.motor_client."""
    assert 'independence_tests.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['independence_tests.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=2)


def test_integration_parametrized_test(testdir: Testdir, read_conftest: str) -> None:
    # pylint: disable=redefined-outer-name
    """Test pytest_motor.plugin.motor_client."""
    assert 'paramatrized_test.py' in test_files.keys()
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(test_files['paramatrized_test.py'].read_text())
    testdir.runpytest().assert_outcomes(passed=3)
