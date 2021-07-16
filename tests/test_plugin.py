"""Test pytest_motor.plugin."""
from asyncio import AbstractEventLoop
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pytest import Testdir

from pytest_motor.plugin import _event_loop


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


def test_motor_client(testdir: Testdir) -> None:
    """Test pytest_motor.plugin.motor_client."""
    testdir.makeconftest("""
    pytest_plugins=["pytest_asyncio", "pytest_motor.plugin"]
    """)

    test_files_directory = Path(__file__).parent.parent / 'test_data' / 'files'
    not_init_file = lambda path: path.name != '__init__.py'
    test_files = filter(not_init_file, test_files_directory.glob('*.py'))

    for test_file in test_files:
        testdir.makepyfile(test_file.read_text())

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
