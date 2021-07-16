"""A test file with a single test that retrieves the Motor client server info."""
import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.mark.asyncio
async def test_using_motor_client_server_info(motor_client: AsyncIOMotorClient) -> None:
    """Test retrieving the Motor client server info."""
    assert await motor_client.server_info() is not None
