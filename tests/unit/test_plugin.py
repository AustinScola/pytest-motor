"""Test pytest_motor.plugin."""
from asyncio import AbstractEventLoop
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pytest_motor.plugin import _database_path, _event_loop

pytestmark = pytest.mark.unit


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


@pytest.mark.asyncio
async def test_database_path(tmp_path: Path) -> None:
    """Test pytest_motor.plugin._database_path."""
    database_path_context = _database_path(tmp_path)

    database_path = await database_path_context.__anext__()
    assert database_path.exists()

    with pytest.raises(StopAsyncIteration):
        await database_path_context.__anext__()
