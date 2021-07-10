"""Test pytest_motor.plugin."""
from pytest import Testdir


def test_motor_client(testdir: Testdir) -> None:
    """Test pytest_motor.plugin.motor_client."""
    testdir.makeconftest("""
    pytest_plugins=["pytest_asyncio", "pytest_motor.plugin"]
    """)

    testdir.makepyfile("""
    from motor.motor_asyncio import AsyncIOMotorClient
    import pytest

    @pytest.mark.asyncio
    async def test_using_motor_client(motor_client: AsyncIOMotorClient) -> None:
       await motor_client.server_info()
    """)

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)
