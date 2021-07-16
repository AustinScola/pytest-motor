"""A pytest plugin which helps test applications using Motor."""
import asyncio
import secrets
import shutil
import socket
import tarfile
from pathlib import Path
from typing import AsyncIterator, Iterator, List

import aiohttp
import pytest
from _pytest.config import Config as PytestConfig
from motor.motor_asyncio import AsyncIOMotorClient


def _event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Yield an event loop.

    This is necessary because pytest-asyncio needs an event loop with a with an equal or higher
    pytest fixture scope as any of the async fixtures. And remember, pytest-asynio is what allows us
    to have async pytest fixtures.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


pytest.fixture(fixture_function=_event_loop, scope='session', name="event_loop")


@pytest.fixture(scope='session')
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Yield an event loop.

    This is necessary because pytest-asyncio needs an event loop with a with an equal or higher
    pytest fixture scope as any of the async fixtures. And remember, pytest-asynio is what allows us
    to have async pytest fixtures.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def root_directory(pytestconfig: PytestConfig) -> Path:
    """Return the root path of pytest."""
    return pytestconfig.rootpath


@pytest.fixture(scope='session')
async def mongod_binary(root_directory: Path) -> Path:  # pylint: disable=redefined-outer-name
    """Return a path to a mongod binary."""
    destination: Path = root_directory.joinpath('.mongod')
    mongod_binary_relative_path = 'mongodb-linux-x86_64-ubuntu1804-4.4.6/bin/mongod'
    mongod_binary_filename = destination.joinpath(mongod_binary_relative_path)

    if not mongod_binary_filename.exists():
        download_url = 'https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.6.tgz'
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as resp:
                with open('binaries.tar', 'wb') as binary_file:
                    # Read by chunks to avoid big RAM consumption
                    while True:
                        # read by 100 bytes
                        chunk = await resp.content.read(100)
                        if not chunk:
                            break
                        binary_file.write(chunk)

        with tarfile.open("binaries.tar") as tar:
            tar.extract(member='mongodb-linux-x86_64-ubuntu1804-4.4.6/bin/mongod', path=destination)

    return mongod_binary_filename


@pytest.fixture(scope='function')
def new_port() -> int:
    """Return an unused port for mongod to run on."""
    port: int = 27017
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as opened_socket:
        opened_socket.bind(("127.0.0.1", 0))  # system will automaticly assign port
        port = opened_socket.getsockname()[1]
    return port


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def databases_directory(root_directory: Path) -> AsyncIterator[Path]:
    """Yield a directory for mongod to store data."""
    databases_directory = root_directory.joinpath('.mongo_databases')
    databases_directory.mkdir(exist_ok=True)

    yield databases_directory


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def database_path(databases_directory: Path) -> AsyncIterator[Path]:
    """Yield a database path for a mongod process to store data."""
    name: str = secrets.token_hex(12)
    database_path: Path = databases_directory.joinpath(name)
    database_path.mkdir()

    yield database_path

    shutil.rmtree(database_path, ignore_errors=True)


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def mongod_socket(new_port: int, database_path: Path,
                        mongod_binary: Path) -> AsyncIterator[str]:
    """Yield a mongod."""
    # yapf: disable
    arguments: List[str] = [
        str(mongod_binary),
        '--port', str(new_port),
        '--storageEngine', 'ephemeralForTest',
        '--logpath', '/dev/null',
        '--dbpath', str(database_path)
    ]
    # yapf: enable

    mongod = await asyncio.create_subprocess_exec(*arguments)

    # mongodb binds to localhost by default
    yield f'localhost:{new_port}'

    try:
        mongod.terminate()
    except ProcessLookupError:
        pass


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def motor_client(mongod_socket: str) -> AsyncIterator[AsyncIOMotorClient]:
    """Yield a Motor client."""
    connection_string = f'mongodb://{mongod_socket}'

    motor_client_: AsyncIOMotorClient = \
        AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=3000)

    yield motor_client_

    motor_client_.close()
