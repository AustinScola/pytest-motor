"""A pytest plugin which helps test applications using Motor."""
import asyncio
import secrets
import shutil
import tarfile
import urllib
import urllib.request
from pathlib import Path
from typing import AsyncIterator, Iterator, List

import pytest
from _pytest.config import Config as PytestConfig
from motor.motor_asyncio import AsyncIOMotorClient


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
    mongod_binary_filename = destination.joinpath(
        'mongodb-linux-x86_64-ubuntu1804-4.4.6/bin/mongod')

    if not mongod_binary_filename.exists():
        download_url = 'https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.6.tgz'
        (tar_filename, _) = urllib.request.urlretrieve(download_url)

        with tarfile.open(tar_filename) as tar:
            tar.extract(member='mongodb-linux-x86_64-ubuntu1804-4.4.6/bin/mongod', path=destination)

        mongod_binary_filename = destination.joinpath(
            'mongodb-linux-x86_64-ubuntu1804-4.4.6/bin/mongod')

    return mongod_binary_filename


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def sockets_directory(root_directory: Path) -> AsyncIterator[Path]:
    """Yield a directory for MongodDB unix sockets."""
    sockets_directory = root_directory.joinpath('.mongod_sockets')
    sockets_directory.mkdir(exist_ok=True)

    yield sockets_directory


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def unix_socket(sockets_directory: Path) -> AsyncIterator[Path]:
    """Yield a random unix socket in the given sockets directory."""
    name: str = secrets.token_hex(12)
    unix_socket = sockets_directory.joinpath(f'{name}.sock')

    yield unix_socket

    try:
        unix_socket.unlink()
    except FileNotFoundError:  # pragma: no cover
        pass


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
async def mongod_socket(unix_socket: Path, database_path: Path,
                        mongod_binary: Path) -> AsyncIterator[Path]:
    """Yield a mongod."""
    arguments: List[str] = [
        str(mongod_binary), '--bind_ip',
        str(unix_socket), '--storageEngine', 'ephemeralForTest', '--fork', '--logpath', '/dev/null',
        '--dbpath',
        str(database_path)
    ]

    mongod = await asyncio.create_subprocess_exec(*arguments)

    yield unix_socket

    try:
        mongod.terminate()
    except ProcessLookupError:
        pass


@pytest.fixture(scope='function')
# pylint: disable=redefined-outer-name
async def motor_client(mongod_socket: Path) -> AsyncIterator[AsyncIOMotorClient]:
    """Yield a Motor client."""
    connection_string = 'mongodb://' + urllib.parse.quote(str(mongod_socket), safe='')

    motor_client_: AsyncIOMotorClient = \
        AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=3000)

    yield motor_client_

    motor_client_.close()
