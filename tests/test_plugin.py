"""Test pytest_motor.plugin."""
from pytest import MonkeyPatch, Testdir, raises

from pytest_motor.plugin import _mongo_ver


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


def test_mongo_ver(monkeypatch: MonkeyPatch) -> None:
    """Test mongo version based on platform system."""
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    assert _mongo_ver() == ("osx", "mongodb-macos-x86_64-4.4.6")

    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert _mongo_ver() == ("linux", "mongodb-linux-x86_64-ubuntu1804-4.4.6")

    monkeypatch.setattr("platform.system", lambda: "Windows")
    with raises(Exception):
        _mongo_ver()
